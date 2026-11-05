#pragma once

#include "../Common.hpp"

namespace packager {

class Imu {
  public:
    Imu();
    Imu(const Vec3 &linearAccel, const Vec3 &angularAccel);

    Vec3 GetLinearAccel() const;
    Vec3 GetAngularVelocity() const;

    void SetLinearAccel(const Vec3 linearAccel);
    void SetAngularVelocity(const Vec3 angularAccel);

  private:
    Vec3 m_LinearAccel;
    Vec3 m_AngularAccel;
};
}; // namespace packager
