
#include "nodes/GenericNode.hpp"
#include "providers/IMUProvider.hpp"
#include <rclcpp/rclcpp.hpp>

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    using namespace std::chrono_literals;
    auto pProvider = std::make_unique<IMUProvider>();

    auto node =
        std::make_shared<GenericNode<IMUProvider, sensor_msgs::msg::Imu>>(
            "ImuTestNode", "imu_test", std::move(pProvider), 8ms);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
