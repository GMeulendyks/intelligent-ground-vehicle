#pragma once
#include <cstddef>
#include <cstdint>
#include <opencv2/core/mat.hpp>
#include <opencv4/opencv2/opencv.hpp>
namespace packager {

struct ImageInfo {
    uint8_t *pData;
    size_t height;
    size_t width;
    int encoding;         // should always be BGRA
    uint8_t channelWidth; // should always be 4
    uint8_t bigEndian;    // ARGB if true
};

class Image {
  public:
    Image();

    Image(ImageInfo info);
    // z-score normalization
    void RunTransformations();

    bool Valid();

    const uint8_t *GetData() const;
    uint8_t *GetData();
    size_t GetLen() const;
    ImageInfo GetInfo() const;

  private:
    uint8_t *m_pData;
    size_t m_Len;
    size_t m_Height;
    size_t m_Width;
    cv::Mat m_Mat;
    bool m_BigEndian;
};
}; // namespace packager
