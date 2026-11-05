#pragma once
#include <filesystem>
#include <string>
class PackagerConfig {
  public:
    PackagerConfig();
    PackagerConfig(const std::string &fn);
    // Parses a file provided in fn
    bool ParseFile(const std::filesystem::path& fn);
    // Parses a string provided in s
    bool Parse(const std::string& s);
    static PackagerConfig Default();
    const std::string &GetCam0Topic();
    const std::string &GetCam1Topic();
    const std::string &GetLidarTopic();
    const std::string &GetImuTopic();

  private:
    std::string m_Cam0;
    std::string m_Cam1;
    std::string m_Lidar;
    std::string m_Imu;
};
