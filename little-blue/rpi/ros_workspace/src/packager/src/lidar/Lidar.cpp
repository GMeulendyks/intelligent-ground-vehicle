#include "packager/lidar/Lidar.hpp"
#include <cmath>
namespace packager {
Lidar::Lidar(LidarScan scan) { ConvertScan(scan); };

void Lidar::ConvertScan(LidarScan scan) {
    m_Points.clear();
    m_Points.reserve(scan.rangeLen);

    float t = 0;
    for (size_t i = 0; i < scan.rangeLen; i++) {
        LidarPoint temp;
        temp.pos.m = scan.rangeData[i];
        if (std::isinf(temp.pos.m)) {
            temp.pos.m = -1.0f;
        }
        temp.pos.t = scan.startAngle + i * scan.angleInc;
        temp.timeFromStart = t;
        t += scan.timeInc;
        // maybe an optimization?
        m_Points.emplace_back(std::move(temp));
    }

    for (size_t i = 0; i < scan.intensityLen; i++) {
        m_Points[i].reflectivity = scan.intensities[i];
    }
};

}; // namespace packager
