#pragma once

#include <sensor_msgs/msg/image.hpp>
#include <string>
#include <opencv4/opencv2/opencv.hpp>
class ImageProvider {
  public:
    ImageProvider(const std::string &fn);

    sensor_msgs::msg::Image Get();

  private:
    sensor_msgs::msg::Image m_Msg;
    cv::Mat m_Img; 
};
