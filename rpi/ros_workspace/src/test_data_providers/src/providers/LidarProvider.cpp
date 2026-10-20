
#include "LidarProvider.hpp"
#include <cstdlib>
LidarProvider::LidarProvider() {
    for(int i = 0; i < 1080; i++) {
        m_Msg.ranges.push_back(1);
    }
};

sensor_msgs::msg::LaserScan LidarProvider::Get() {
    for (auto& r : m_Msg.ranges) {
        r = std::rand() * 1.0 / RAND_MAX;
    }

    return m_Msg;
}
