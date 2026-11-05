#pragma once

#include <sensor_msgs/msg/imu.hpp>
class IMUProvider {
  public:
    IMUProvider();

    sensor_msgs::msg::Imu Get();

  private:
    sensor_msgs::msg::Imu m_Msg;
};
