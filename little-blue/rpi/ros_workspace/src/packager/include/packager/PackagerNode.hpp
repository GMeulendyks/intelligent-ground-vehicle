
#pragma once
#include "Packager.hpp"
#include "img/Image.hpp"
#include "lidar/Lidar.hpp"
#include "packager/imu/Imu.hpp"
#include "packager_msgs/msg/package.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

class PackagerNode : public rclcpp::Node {
    using Packager = packager::Packager<packager::Image, packager::Image,
                                        packager::Lidar, packager::Imu>;

  public:
    PackagerNode(const std::string &cam0, const std::string &cam1,
                 const std::string &lidar, const std::string &imu);

  private:
    Packager m_Packager;
    rclcpp::Publisher<packager_msgs::msg::Package>::SharedPtr m_Publisher;
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr m_Cam0;
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr m_Cam1;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr m_Lidar;
    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr m_Imu;

    void Cam0Sub(sensor_msgs::msg::Image);
    void Cam1Sub(sensor_msgs::msg::Image);
    void LidarSub(sensor_msgs::msg::LaserScan);
    void ImuSub(sensor_msgs::msg::Imu);
    void PackagePublish(const Packager::Package&);
};
