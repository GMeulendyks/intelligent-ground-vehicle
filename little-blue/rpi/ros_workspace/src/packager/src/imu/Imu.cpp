#include "packager/imu/Imu.hpp"


namespace packager {

    Imu::Imu() {};
    Imu::Imu(const Vec3& linearAccel, const Vec3& angularAccel) :
                m_LinearAccel(linearAccel), m_AngularAccel(angularAccel) {}
            // yeah yeah sue me for putting the implementation in the header
            // for an empty constructor

            Vec3 Imu::GetLinearAccel() const { return m_LinearAccel; }
            Vec3 Imu::GetAngularVelocity() const { return m_AngularAccel; }

            void Imu::SetLinearAccel(const Vec3 linearAccel) { m_LinearAccel = linearAccel; }
            void Imu::SetAngularVelocity(const Vec3 angularAccel) { m_AngularAccel = angularAccel; }
}
