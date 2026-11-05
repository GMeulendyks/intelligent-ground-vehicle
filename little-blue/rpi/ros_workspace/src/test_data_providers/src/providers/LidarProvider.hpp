
#pragma once

#include <sensor_msgs/msg/laser_scan.hpp>
class LidarProvider {
  public:
    LidarProvider();

    sensor_msgs::msg::LaserScan Get();

  private:
    sensor_msgs::msg::LaserScan m_Msg;
};
