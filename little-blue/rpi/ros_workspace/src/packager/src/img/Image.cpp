#include "packager/img/Image.hpp"
#include <opencv2/core.hpp>
#include <opencv2/core/mat.hpp>
#include <opencv2/imgproc.hpp>

namespace packager {
Image::Image() : m_pData(nullptr), m_Len(0), m_Mat() {}

Image::Image(ImageInfo info)
    : m_pData(info.pData), m_Len(info.width * info.height * info.channelWidth),
      m_Height(info.height), m_Width(info.width), m_BigEndian(info.bigEndian) {
    uint8_t channel = info.channelWidth == 3 ? CV_8UC3 : CV_8UC4;
    cv::Mat(info.height, info.width, channel, info.pData).copyTo(m_Mat);
    if (info.channelWidth != 3) {
        if (info.bigEndian) {
            cv::cvtColor(m_Mat, m_Mat, cv::COLOR_BGRA2BGR);
        } else {
            cv::cvtColor(m_Mat, m_Mat, cv::COLOR_RGBA2RGB);
        }
    }
}

bool Image::Valid() { return !m_pData; }

void Image::RunTransformations() {
    // there was originally meant to be more here
    // and in the future there might be
    const float topPercent = 0.6f;
    size_t top = m_Mat.rows * topPercent;
    size_t roiHeight = m_Mat.rows * (1.0f - topPercent);
    m_Mat = cv::Mat(m_Mat, cv::Rect(cv::Point(0, top), cv::Size(m_Mat.cols, roiHeight)));
    cv::resize(m_Mat, m_Mat, cv::Size(256, 256), 0.0, 0.0, cv::INTER_LINEAR);
    cv::cvtColor(m_Mat, m_Mat, cv::COLOR_RGB2GRAY);
}

uint8_t *Image::GetData() { return m_Mat.data; }
size_t Image::GetLen() const { return m_Mat.cols * m_Mat.rows; }
ImageInfo Image::GetInfo() const {
    ImageInfo ret;
    ret.pData = m_Mat.data;
    ret.height = m_Mat.rows;
    ret.width = m_Mat.cols;
    ret.channelWidth = m_Mat.channels();
    ret.encoding = 2;

    return ret;
}
}; // namespace packager
