#include "ImageProvider.hpp"
#include <exception>
#include <opencv2/opencv.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <opencv2/imgcodecs.hpp>

ImageProvider::ImageProvider(const std::string &fn)
: m_Img(cv::imread(fn)) {

    // imread always produces a BGR, 8UC3 image by default
    if (!m_Img.data) {
        std::cerr << "Failed to read file: " << fn << '\n';
        throw std::runtime_error("Failed reading file. Exiting.");
    }
    m_Msg.data = std::vector(m_Img.data, m_Img.data + (m_Img.channels() * m_Img.rows * m_Img.cols));
    m_Msg.width = m_Img.cols;
    m_Msg.height = m_Img.rows;
    m_Msg.encoding = sensor_msgs::image_encodings::BGR8;
    m_Msg.is_bigendian = 0;
}

sensor_msgs::msg::Image ImageProvider::Get() {
    return m_Msg;    
}
