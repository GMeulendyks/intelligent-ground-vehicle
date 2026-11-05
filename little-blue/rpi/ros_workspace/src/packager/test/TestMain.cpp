#include "packager/PackagerConfig.hpp"
#include <gtest/gtest.h>

#ifdef CONF_FP
TEST(packager, config_file_test) {

    PackagerConfig conf;
    ASSERT_TRUE(conf.ParseFile(CONF_FP));

    auto defaultConfig = PackagerConfig::Default();
    ASSERT_EQ(defaultConfig.GetImuTopic(), conf.GetImuTopic());
    ASSERT_EQ(defaultConfig.GetCam0Topic(), conf.GetCam0Topic());
    ASSERT_EQ(defaultConfig.GetCam1Topic(), conf.GetCam1Topic());
    ASSERT_EQ(defaultConfig.GetLidarTopic(), conf.GetLidarTopic());
}
#endif

TEST(packager, config_string_test) {

    auto default_conf = R"(
topics:
  cam0: "usb_cam_0/image_raw"
  cam1: "usb_cam_1/image_raw"
  imu: "imu/data"
  lidar: "rplidarNode/scan"
)";

    PackagerConfig conf;
    ASSERT_TRUE(conf.Parse(default_conf));

    auto defaultConfig = PackagerConfig::Default();
    ASSERT_EQ(defaultConfig.GetImuTopic(), conf.GetImuTopic());
    ASSERT_EQ(defaultConfig.GetCam0Topic(), conf.GetCam0Topic());
    ASSERT_EQ(defaultConfig.GetCam1Topic(), conf.GetCam1Topic());
    ASSERT_EQ(defaultConfig.GetLidarTopic(), conf.GetLidarTopic());
}

int main(int argc, char **argv) {

    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
