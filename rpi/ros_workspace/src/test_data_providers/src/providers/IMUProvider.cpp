
#include "IMUProvider.hpp"
#include <random>
IMUProvider::IMUProvider() {}

sensor_msgs::msg::Imu IMUProvider::Get() {
    m_Msg.linear_acceleration.x = rand() * 1.0 / RAND_MAX;
    m_Msg.linear_acceleration.y = rand() * 1.0 / RAND_MAX;
    m_Msg.linear_acceleration.z = rand() * 1.0 / RAND_MAX;

    m_Msg.angular_velocity.x = rand() * 1.0 / RAND_MAX;
    m_Msg.angular_velocity.y = rand() * 1.0 / RAND_MAX;
    m_Msg.angular_velocity.z = rand() * 1.0 / RAND_MAX;

    return m_Msg;
}
