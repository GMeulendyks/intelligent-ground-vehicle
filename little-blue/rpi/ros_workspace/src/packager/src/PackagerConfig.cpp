#include "packager/PackagerConfig.hpp"
#include "yaml-cpp/exceptions.h"
#include "yaml-cpp/yaml.h"
#include <iostream>
PackagerConfig::PackagerConfig() {}
PackagerConfig::PackagerConfig(const std::string &fn) {

    Parse(fn);

}

bool PackagerConfig::ParseFile(const std::filesystem::path& fn) {
    try {
        YAML::Node config = YAML::LoadFile(fn);
        YAML::Node topics = config["topics"];

        m_Cam0 = topics["cam0"].as<std::string>();
        m_Cam1 = topics["cam1"].as<std::string>();
        m_Imu = topics["imu"].as<std::string>();
        m_Lidar = topics["lidar"].as<std::string>();
    } catch (YAML::Exception e) {
        std::cerr << e.what();
        return false;
    }
    return true;
}

bool PackagerConfig::Parse(const std::string& s) {
    try {
        YAML::Node config = YAML::Load(s);
        YAML::Node topics = config["topics"];

        std::cerr << "Topics: " << topics << '\n';

        m_Cam0 = topics["cam0"].as<std::string>();
        m_Cam1 = topics["cam1"].as<std::string>();
        m_Imu = topics["imu"].as<std::string>();
        m_Lidar = topics["lidar"].as<std::string>();
    } catch (YAML::Exception e) {
        std::cerr << e.what();
        return false;
    }
    return true;
}

PackagerConfig PackagerConfig::Default() {
    PackagerConfig ret;
    ret.m_Cam0 = "usb_cam_0/image_raw";
    ret.m_Cam1 = "usb_cam_1/image_raw";
    ret.m_Imu = "imu/data";
    ret.m_Lidar = "rplidarNode/scan";

    return ret;
}
const std::string &PackagerConfig::GetCam0Topic() { return m_Cam0; }
const std::string &PackagerConfig::GetCam1Topic() { return m_Cam1; }
const std::string &PackagerConfig::GetLidarTopic() { return m_Lidar; }
const std::string &PackagerConfig::GetImuTopic() { return m_Imu; }
