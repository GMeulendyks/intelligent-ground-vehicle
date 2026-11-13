/*****************************************************************************
 * Local addition (LittleBlue): cheap, Bayer-aware resolution reduction.
 *
 * Header-only and free of ROS / pylon / OpenCV dependencies so it can be
 * unit-tested on its own.
 *
 * Why: the a2A3840-45ucBAS has no on-camera binning. Reducing the raw Bayer
 * mosaic *before* debayering and publishing means the Jetson never has to
 * serialise, copy and colour-convert full 4K frames.
 *
 * Method ("super-pixel" reduction): every 2x2 Bayer cell becomes one BGR
 * pixel (R, mean of the two greens, B). No interpolation is involved, so this
 * is equivalent to a same-colour 2x2 binning. For a factor of 4 the output
 * pixel is the mean over a 2x2 block of those cells (i.e. 4x4 raw pixels).
 *****************************************************************************/
#ifndef PYLON_ROS2_CAMERA__IMAGE_REDUCTION_HPP_
#define PYLON_ROS2_CAMERA__IMAGE_REDUCTION_HPP_

#include <cstddef>
#include <cstdint>
#include <string>

namespace pylon_ros2_camera
{

/**
 * @brief Positions inside a 2x2 Bayer cell, indexed row-major:
 *        0 = (row 0, col 0), 1 = (0, 1), 2 = (1, 0), 3 = (1, 1).
 * @param encoding sensor_msgs encoding string, e.g. "bayer_rggb8"
 * @return false if the encoding is not an 8-bit Bayer encoding.
 */
inline bool bayerCellLayout(const std::string& encoding, int& r, int& g1, int& g2, int& b)
{
  if (encoding == "bayer_rggb8")      { r = 0; g1 = 1; g2 = 2; b = 3; return true; }
  else if (encoding == "bayer_bggr8") { b = 0; g1 = 1; g2 = 2; r = 3; return true; }
  else if (encoding == "bayer_gbrg8") { g1 = 0; b = 1; r = 2; g2 = 3; return true; }
  else if (encoding == "bayer_grbg8") { g1 = 0; r = 1; b = 2; g2 = 3; return true; }
  return false;
}

/**
 * @brief Reduce an 8-bit Bayer mosaic to a BGR8 image.
 *
 * @param src       Bayer data (row 0 first).
 * @param src_step  Bytes per source row.
 * @param out_w     Output width  (= src_width  / scale).
 * @param out_h     Output height (= src_height / scale).
 * @param scale     2 or 4. The caller guarantees src_width and src_height are
 *                  divisible by scale.
 * @param r,g1,g2,b Cell layout from bayerCellLayout().
 * @param dst       Output buffer, out_w * out_h * 3 bytes, tightly packed (BGR).
 */
inline void bayer8ToBgr8Reduce(const std::uint8_t* src, std::size_t src_step,
                               std::size_t out_w, std::size_t out_h, int scale,
                               int r, int g1, int g2, int b, std::uint8_t* dst)
{
  if (scale == 2)
  {
    for (std::size_t y = 0; y < out_h; ++y)
    {
      const std::uint8_t* row0 = src + (2 * y) * src_step;
      const std::uint8_t* row1 = row0 + src_step;
      std::uint8_t* d = dst + y * out_w * 3;
      for (std::size_t x = 0; x < out_w; ++x)
      {
        const std::uint8_t c[4] = {row0[2 * x], row0[2 * x + 1], row1[2 * x], row1[2 * x + 1]};
        d[3 * x + 0] = c[b];
        d[3 * x + 1] = static_cast<std::uint8_t>((static_cast<unsigned>(c[g1]) + c[g2] + 1u) >> 1);
        d[3 * x + 2] = c[r];
      }
    }
    return;
  }

  // Generic path (used for scale == 4): average the cells inside each block.
  const std::size_t cells = static_cast<std::size_t>(scale) / 2;  // cells per side
  const unsigned n = static_cast<unsigned>(cells * cells);
  for (std::size_t y = 0; y < out_h; ++y)
  {
    std::uint8_t* d = dst + y * out_w * 3;
    for (std::size_t x = 0; x < out_w; ++x)
    {
      unsigned sr = 0, sg = 0, sb = 0;
      for (std::size_t cy = 0; cy < cells; ++cy)
      {
        const std::uint8_t* row0 = src + (2 * (y * cells + cy)) * src_step;
        const std::uint8_t* row1 = row0 + src_step;
        for (std::size_t cx = 0; cx < cells; ++cx)
        {
          const std::size_t col = 2 * (x * cells + cx);
          const std::uint8_t c[4] = {row0[col], row0[col + 1], row1[col], row1[col + 1]};
          sr += c[r];
          sb += c[b];
          sg += static_cast<unsigned>(c[g1]) + c[g2];
        }
      }
      d[3 * x + 0] = static_cast<std::uint8_t>((sb + n / 2) / n);
      d[3 * x + 1] = static_cast<std::uint8_t>((sg + n) / (2 * n));  // 2n greens, round to nearest
      d[3 * x + 2] = static_cast<std::uint8_t>((sr + n / 2) / n);
    }
  }
}

/**
 * @brief Box-average reduction for interleaved 8-bit images (mono8: channels = 1,
 *        bgr8/rgb8: channels = 3). Channel order is preserved.
 *
 * @param src      Source pixels.
 * @param src_step Bytes per source row.
 * @param out_w    Output width  (= src_width  / scale).
 * @param out_h    Output height (= src_height / scale).
 * @param scale    Integer reduction factor; caller guarantees divisibility.
 * @param channels Interleaved channels per pixel.
 * @param dst      Output buffer, out_w * out_h * channels bytes, tightly packed.
 */
inline void box8Reduce(const std::uint8_t* src, std::size_t src_step,
                       std::size_t out_w, std::size_t out_h, int scale, int channels,
                       std::uint8_t* dst)
{
  const std::size_t sc = static_cast<std::size_t>(scale);
  const std::size_t ch = static_cast<std::size_t>(channels);
  const unsigned n = static_cast<unsigned>(sc * sc);
  for (std::size_t y = 0; y < out_h; ++y)
  {
    std::uint8_t* d = dst + y * out_w * ch;
    for (std::size_t x = 0; x < out_w; ++x)
    {
      for (std::size_t c = 0; c < ch; ++c)
      {
        unsigned sum = 0;
        for (std::size_t dy = 0; dy < sc; ++dy)
        {
          const std::uint8_t* row = src + (y * sc + dy) * src_step + (x * sc) * ch + c;
          for (std::size_t dx = 0; dx < sc; ++dx)
          {
            sum += row[dx * ch];
          }
        }
        d[x * ch + c] = static_cast<std::uint8_t>((sum + n / 2) / n);
      }
    }
  }
}

}  // namespace pylon_ros2_camera

#endif  // PYLON_ROS2_CAMERA__IMAGE_REDUCTION_HPP_
