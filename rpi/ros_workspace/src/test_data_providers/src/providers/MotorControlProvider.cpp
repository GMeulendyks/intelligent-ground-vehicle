#include "MotorControlProvider.hpp"

MotorControlProvider::MotorControlProvider() {}

packager_msgs::msg::MotorControl MotorControlProvider::Get() { 
    static bool reverse = false;

    if (reverse) {
        m_Msg.throttle = -0.05;
    } else {
        m_Msg.throttle = 0.05;
    }

    reverse = !reverse;

}
