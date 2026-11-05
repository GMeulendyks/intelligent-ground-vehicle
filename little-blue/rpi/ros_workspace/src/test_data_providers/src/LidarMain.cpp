
#include "nodes/GenericNode.hpp"
#include "providers/LidarProvider.hpp"
#include <rclcpp/rclcpp.hpp>

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    using namespace std::chrono_literals;
    auto pProvider = std::make_unique<LidarProvider>();

    auto node =
        std::make_shared<GenericNode<LidarProvider, sensor_msgs::msg::LaserScan>>(
            "LidarTestNode", "lidar_test", std::move(pProvider), 100ms);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
