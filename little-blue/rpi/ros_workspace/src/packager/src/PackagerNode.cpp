#include "packager/PackagerNode.hpp"
#include "packager/Common.hpp"
#include "packager/imu/Imu.hpp"
#include "packager/lidar/Lidar.hpp"
#include "sensor_msgs/image_encodings.hpp"
#include <functional>
#include <packager_msgs/msg/detail/lidar_sample__struct.hpp>

PackagerNode::PackagerNode(const std::string &cam0, const std::string &cam1,
                           const std::string &lidar, const std::string &imu)
    : Node("packager") {

    using std::placeholders::_1;

    m_Publisher =
        create_publisher<packager_msgs::msg::Package>("packages", 10);
    m_Cam0 = create_subscription<sensor_msgs::msg::Image>(
        cam0, 10, std::bind(&PackagerNode::Cam0Sub, this, _1));
    m_Cam1 = create_subscription<sensor_msgs::msg::Image>(
        cam1, 10, std::bind(&PackagerNode::Cam1Sub, this, _1));
    m_Imu = create_subscription<sensor_msgs::msg::Imu>(
        imu, 10, std::bind(&PackagerNode::ImuSub, this, _1));
    m_Lidar = create_subscription<sensor_msgs::msg::LaserScan>(
        lidar, 10, std::bind(&PackagerNode::LidarSub, this, _1));

    m_Packager.Register(std::bind(&PackagerNode::PackagePublish, this, _1));

}

void PackagerNode::Cam0Sub(sensor_msgs::msg::Image img) {

    packager::ImageInfo info;
    if (img.data.size() == 0 || img.width == 0 || img.height == 0)
    {
        // For some reason, the image can be empty?
        return;
    }
    info.pData = img.data.data();
    info.width = img.width;
    info.height = img.height;
    info.bigEndian = img.is_bigendian;
    info.channelWidth = sensor_msgs::image_encodings::numChannels(img.encoding);
    info.encoding = 1; // unused for now, always assumed to be BGRA
    packager::Image im(info);
    im.RunTransformations();
    m_Packager.Set<0>(std::move(im));
}
void PackagerNode::Cam1Sub(sensor_msgs::msg::Image img) {
    packager::ImageInfo info;
    if (img.data.size() == 0 || img.width == 0 || img.height == 0)
    {
        // For some reason, the image can be empty?
        return;
    }
    info.pData = img.data.data();
    info.width = img.width;
    info.height = img.height;
    info.bigEndian = img.is_bigendian;
    info.channelWidth = sensor_msgs::image_encodings::numChannels(img.encoding);
    info.encoding = 1; // unused for now, always assumed to be BGRA
    packager::Image im(info);
    im.RunTransformations();
    m_Packager.Set<1>(std::move(im));
}
void PackagerNode::LidarSub(sensor_msgs::msg::LaserScan scan) {

    packager::LidarScan lscan;
    lscan.timeInc = scan.time_increment;
    lscan.scanTime = scan.scan_time;
    lscan.angleInc = scan.angle_increment;
    lscan.startAngle = scan.angle_min;
    lscan.rangeData = scan.ranges.data();
    lscan.rangeLen = scan.ranges.size();
    lscan.intensities = scan.intensities.data();
    lscan.intensityLen = scan.intensities.size();

    m_Packager.Set<2>(packager::Lidar(lscan));
}
void PackagerNode::ImuSub(sensor_msgs::msg::Imu imu) {

    packager::Vec3 lin_accel;
    lin_accel.x = imu.linear_acceleration.x;
    lin_accel.y = imu.linear_acceleration.y;
    lin_accel.z = imu.linear_acceleration.z;

    packager::Vec3 ang_vel;
    ang_vel.x = imu.angular_velocity.x;
    ang_vel.y = imu.angular_velocity.y;
    ang_vel.z = imu.angular_velocity.z;

    m_Packager.Set<3>(packager::Imu(lin_accel, ang_vel));
}
void PackagerNode::PackagePublish(const Packager::Package& pkg) {

    packager_msgs::msg::Package msg;

    // IMU
    auto& imu = std::get<3>(pkg);
    packager::Vec3 lin_accel = imu.GetLinearAccel();
    packager::Vec3 ang_vel = imu.GetAngularVelocity();
    msg.linear_acceleration.x = lin_accel.x;
    msg.linear_acceleration.y = lin_accel.y;
    msg.linear_acceleration.z = lin_accel.z;

    msg.angular_velocity.x = ang_vel.x;
    msg.angular_velocity.y = ang_vel.y;
    msg.angular_velocity.z = ang_vel.z;

    // CAM0
    packager::ImageInfo info = std::get<0>(pkg).GetInfo();
    msg.cam0.assign(info.pData, info.pData + (info.channelWidth *
                                                   info.width * info.height));

    msg.cam_width = info.width;
    msg.cam_height = info.height;
    // CAM1
    info = std::get<1>(pkg).GetInfo();
    msg.cam1.assign(info.pData, info.pData + (info.channelWidth *
                                                   info.width * info.height));
    // LIDAR
    auto cloud = std::get<2>(pkg).GetPoints();
    packager_msgs::msg::LidarSample sample;
    for (auto point : cloud) {
        sample.magnitude = point.pos.m;
        sample.angle = point.pos.t;
        sample.intensity = point.reflectivity;
        msg.lidar_samples.push_back(std::move(sample));
    }

    std::cerr << "Publishing package.\n";
    m_Publisher->publish(msg);

}
