#pragma once
#include "../Common.hpp"
#include <cstddef>
#include <vector>


namespace packager {

    struct LidarPoint {
        Polar2 pos;
        float reflectivity;
        float timeFromStart;
    };

    struct LidarScan {
        size_t rangeLen;
        float* rangeData;
        size_t intensityLen;
        float* intensities;
        float startAngle;
        float angleInc;
        float timeInc;
        float scanTime;
    };

    class Lidar {
        public:
            Lidar() {};
            Lidar(LidarScan scan);

            void ConvertScan(LidarScan scan);
            const std::vector<LidarPoint>& GetPoints() const { return m_Points; }
        private:
        std::vector<LidarPoint> m_Points;

    };
};
