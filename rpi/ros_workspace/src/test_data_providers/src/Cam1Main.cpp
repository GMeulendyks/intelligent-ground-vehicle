
#include "nodes/GenericNode.hpp"
#include "providers/ImageProvider.hpp"
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/detail/image__struct.hpp>

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    using namespace std::chrono_literals;
    auto imgpath = std::getenv("TEST_IMG_PATH");
    if (!imgpath) {
        std::cerr << "Error finding image path.\n";
        return -1;
    }
    auto pProvider = std::make_unique<ImageProvider>(imgpath);

    auto node =
        std::make_shared<GenericNode<ImageProvider, sensor_msgs::msg::Image>>(
            "Cam1Node", "cam1_test", std::move(pProvider), 16.6ms);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
