
#include "packager/PackagerConfig.hpp"
#include "packager/PackagerNode.hpp"
#include <cstdlib>

int main(int argc, char **argv) {
    PackagerConfig conf;
    char *envConfig = std::getenv("PACKAGER_CONF");

    if (!conf.ParseFile(envConfig)) {
        std::cerr << "Environment Variable configuration failed...\n";
        if (!conf.ParseFile("config/default.yaml")) {
            std::cerr << "All paths failed. Using default configuration\n";
            conf = PackagerConfig::Default();
        }
    }

    rclcpp::init(argc, argv);
    // In future, change spin to a multithreaded executor if it helps
    // also, maybe change to wait_on_future or whatever it's called
    // to ensure we can close if a signal is given
    rclcpp::spin(std::make_shared<PackagerNode>(
        conf.GetCam0Topic(), conf.GetCam1Topic(), conf.GetLidarTopic(),
        conf.GetImuTopic()));
    rclcpp::shutdown();

    return 0;
}
