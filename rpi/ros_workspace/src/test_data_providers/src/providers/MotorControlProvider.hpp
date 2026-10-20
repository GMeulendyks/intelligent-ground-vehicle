#pragma once
#include "packager_msgs/msg/motor_control.hpp"
class MotorControlProvider {
  public:
    MotorControlProvider();

    packager_msgs::msg::MotorControl Get();

  private:
    packager_msgs::msg::MotorControl m_Msg;
};
