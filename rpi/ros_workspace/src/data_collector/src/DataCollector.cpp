#include <chrono>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <mutex>
#include <opencv2/opencv.hpp>
#include <packager_msgs/msg/package.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <utils/threading/Threading.hpp>

namespace node {
using namespace packager_msgs::msg;
using namespace sensor_msgs::msg;
using std::placeholders::_1;

constexpr uint8_t JOYSTICK_STEERING_AXIS = 0;
constexpr uint8_t JOYSTICK_THROTTLE_AXIS = 5;
constexpr uint8_t JOYSTICK_START_BUTTON = 7;

class DataCollector {
  public:
    DataCollector(std::string_view dataPath) : m_Index(0), m_JoyData({}), m_DataPath(dataPath){
        using namespace std::chrono;
        auto now = std::chrono::system_clock::now();

        auto unixTimestamp =
            duration_cast<seconds>(now.time_since_epoch()).count();

        std::stringstream ss;

        ss << m_DataPath << '/' << unixTimestamp;

        m_Path = ss.str();

        std::filesystem::create_directories(m_Path);
        std::filesystem::create_directory(m_Path / "cam0");
        std::filesystem::create_directory(m_Path / "cam1");
        std::filesystem::create_directory(m_Path / "lidar");

        auto imupath = m_Path / "imu.csv";
        auto joypath = m_Path / "joy.csv";

        m_JoyFile = std::ofstream(joypath);
        m_ImuFile = std::ofstream(imupath);

        m_ThreadPool.Run();
    };

    void Reset() {
        using namespace std::chrono;
        auto now = std::chrono::system_clock::now();

        auto unixTimestamp =
            duration_cast<seconds>(now.time_since_epoch()).count();

        std::stringstream ss;

        ss << m_DataPath << '/' << unixTimestamp;

        m_Path = ss.str();

        m_JoyFile.close();
        m_ImuFile.close();

        auto imupath = m_Path / "imu.csv";
        auto joypath = m_Path / "joy.csv";

        m_ImuFile = std::ofstream(imupath);
        m_JoyFile = std::ofstream(joypath);
    }

    void SetPackage(Package &pkg) {
        std::cerr << "Writing Package " << m_Index << '\n';
        JoyData tempJoy;
        {
            std::unique_lock l(m_JoyDataMutex);
            tempJoy = m_JoyData;
        }

        auto lidarpath = m_Path / "lidar/";
        auto cam0path = m_Path / "cam0/";
        auto cam1path = m_Path / "cam1/";

        // eg: m_Index = 25 -> path/0000000025
        auto getFilename = [this](auto &path, auto &ext) {
            std::stringstream ss;
            ss << std::setw(10) << std::setfill('0') << m_Index << ext;
            auto ret = path / ss.str();
            return ret;
        };

        CamData data;
        data.cam0 = std::move(pkg.cam0);
        data.cam1 = std::move(pkg.cam1);
        data.cam0path = std::move(getFilename(cam0path, ".jpg"));
        data.cam1path = std::move(getFilename(cam1path, ".jpg"));
        data.cam_height = pkg.cam_height;
        data.cam_width = pkg.cam_width;

        m_ThreadPool.Submit({data, [](igvc::JobData &data) {
            CamData camData = data.as<CamData>();

            cv::Mat cam0(camData.cam_height, camData.cam_width, CV_8UC1, camData.cam0.data());
            cv::Mat cam1(camData.cam_height, camData.cam_width, CV_8UC1, camData.cam1.data());

            cv::imwrite(camData.cam0path, cam0);
            cv::imwrite(camData.cam1path, cam1);

        }});

        std::ofstream lidarFile(getFilename(lidarpath, ".csv"));
        for (auto &pt : pkg.lidar_samples) {
            lidarFile << pt.magnitude << ',' << pt.angle << ',' << pt.intensity << '\n';
        }
        lidarFile.close();

        auto la = pkg.linear_acceleration;
        // in the future maybe we'll use rotational velocity
        m_ImuFile << la.x << ',' << la.y << ',' << la.z << '\n';

        m_JoyFile << tempJoy.throttle << ',' << tempJoy.steering << '\n';
        m_Index++;
    }

    void SetJoystick(Joy joystick) {
        std::unique_lock l(m_JoyDataMutex);
        m_JoyData.steering = joystick.axes.at(JOYSTICK_STEERING_AXIS);
        m_JoyData.throttle = joystick.axes.at(JOYSTICK_THROTTLE_AXIS);
    }

  private:
    struct JoyData {
        float steering; // Raw joystick steering
        float throttle; // Raw joystick throttle
    };

    struct CamData {
        std::vector<uint8_t> cam0;
        std::vector<uint8_t> cam1;
        std::string cam0path;
        std::string cam1path;
        uint32_t cam_width;
        uint32_t cam_height;
    };

    // joystick is gonna be extremely fast.
    JoyData m_JoyData;
    std::mutex m_JoyDataMutex;

    std::string m_DataPath;

    std::ofstream m_JoyFile;
    std::ofstream m_ImuFile;

    // used just for "this collection period"
    std::atomic<size_t> m_Index;
    std::filesystem::path m_Path;


    igvc::ThreadPool<4> m_ThreadPool;

    static cv::Mat GetGrayscaleImage(std::vector<uint8_t> &vals, uint32_t width,
                                     uint32_t height) {
        // images are -1 to 1, convert to 0 to 255 with negative wrapping
        // it's fucked up and weird and it's only so we get a somewhat visible
        // look at the images.
        cv::Mat cvt;
        cv::Mat(height, width, CV_32FC1, vals.data()).copyTo(cvt);
        cvt.forEach<float>([](float &pixel, const int *) {
            if (pixel < 0.0) {
                pixel = pixel - (int)pixel;
                pixel = (int)(255 - (pixel * -255)) % 255;
            } else {
                pixel = (int)(pixel * 255) % 255;
            }
        });
        cvt.convertTo(cvt, CV_8UC1);
        return cvt;
    }
};

class DataCollectorNode : public rclcpp::Node {
  public:
    DataCollectorNode(std::string_view dataPath) : Node("data_collector"), m_Collector(dataPath), m_Collect(false), m_PrevStart(false) {
        m_pPackager = create_subscription<Package>(
            "packages", 10,
            std::bind(&DataCollectorNode::PackagerCallback, this, _1));
        m_pJoystick = create_subscription<Joy>(
            "joy", 10,
            std::bind(&DataCollectorNode::JoystickCallback, this, _1));

        if (std::filesystem::exists(dataPath) == false) {
            std::filesystem::create_directory(dataPath);
        }

    }

  private:
    rclcpp::Subscription<Package>::SharedPtr m_pPackager;
    rclcpp::Subscription<Joy>::SharedPtr m_pJoystick;

    DataCollector m_Collector;

    std::atomic<bool> m_Collect;

    bool m_PrevStart = false;

    void PackagerCallback(Package pkg) {
        if (m_Collect) {
            m_Collector.SetPackage(pkg);
        }
    }

    void JoystickCallback(Joy joystick) {
        if (joystick.buttons.at(JOYSTICK_START_BUTTON)) {
            m_PrevStart = true;
        } else if (m_PrevStart == true && !joystick.buttons.at(JOYSTICK_START_BUTTON)) {
            m_Collect = !m_Collect;
            m_PrevStart = false;
        }

        if (m_Collect)
            m_Collector.SetJoystick(joystick);
    }
};

}; // namespace node

int main(int argc, char **argv) {
	const char* envPath = std::getenv("DATA_COLLECTION_PATH");
	std::string_view dataPath = "data_collection";
	if (envPath) {
		dataPath = envPath;
	}
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<node::DataCollectorNode>(dataPath));
    rclcpp::shutdown();
    return 0;
}
