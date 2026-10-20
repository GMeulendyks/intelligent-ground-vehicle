#include "nodes/GenericNode.hpp"
#include "providers/MotorControlProvider.hpp"
#include <rclcpp/rclcpp.hpp>

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    using namespace std::chrono_literals;
    auto pProvider = std::make_unique<MotorControlProvider>();

    auto node = std::make_shared<
        GenericNode<MotorControlProvider, packager_msgs::msg::MotorControl>>(
        "MotorControlTest", "motor_control", std::move(pProvider), 250ms);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
