#include <rclcpp/rclcpp.hpp>
#include <memory>
#include <iostream>
#include <packager_msgs/msg/gps.hpp>
#include <math.h>

#include <GeographicLib/UTMUPS.hpp>
#include <geometry_msgs/msg/vector3.hpp>
#include <cmath>
namespace node {
    using namespace geometry_msgs::msg;
    using namespace packager_msgs::msg;
    struct Vec2{
        double x,y;

        Vec2() : x(0.0), y(0.0) {}
        Vec2(float longitude, float latitude): x(longitude), y(latitude) {}
        Vec2(const Vector3& v): x(v.x), y(v.y) {}

        static Vec2 utm_from_latlong(float longitude, float latitude) {
            double easting;
            double northing;
            int zone;
            bool northp;
            double gamma;
            double k;
            GeographicLib::UTMUPS::Forward(latitude, longitude, zone, northp, easting, northing, gamma, k);
            return Vec2(easting, northing);
        }
        float dot(const Vec2& o) const {
            return x*o.x + y*o.y;
        }
        float mag() const {
            return std::sqrt(x*x + y*y);
        }
        float angle_between(const Vec2& o) const {
            return std::acos(dot(o) / (mag() * o.mag()));
        }
        float distance_between(const Vec2& o) const {
            return std::sqrt((x - o.x)*(x - o.x) + (y - o.y)*(y - o.y)); 
        }
        Vec2 operator-(const Vec2& o) const {
            return Vec2(x - o.x, y - o.y);
        }
        bool operator==(const Vec2& o) const {
            return x == o.x && y == o.y;
        }
    };

    class GpsNode : public rclcpp::Node {

        public:
            GpsNode() : Node("gps"), m_PrevDir(Vec2(0.0f,0.0f)) {
                using std::placeholders::_1;
                m_pBelforeSubscription = create_subscription<Vector3>("odu/fix", 1, std::bind(&GpsNode::GpsCallback, this, _1));
                m_pGpsPublisher = create_publisher<Gps>("gps", 1);
                m_Waypoints = {{318129.25506070675, 4726349.1617945405}};
                m_WaypointsIter = m_Waypoints.begin();
                m_Waypoint = *m_WaypointsIter++;
            }

        private:

            Vec2 m_PrevDir;
            Vec2 m_Waypoint;
            std::vector<Vec2> m_Waypoints;
            std::vector<Vec2>::const_iterator m_WaypointsIter;
            float k = 0.004f;

            rclcpp::Subscription<Vector3>::SharedPtr m_pBelforeSubscription;
            rclcpp::Publisher<Gps>::SharedPtr m_pGpsPublisher;

            void GpsCallback(Vector3 vec) {
                static constexpr float throttle = 0.08f;
                if (m_PrevDir == Vec2(0.0,0.0)) {
                    std::cerr << "Setting first sample...\n";
                    m_PrevDir = Vec2::utm_from_latlong(vec.y, vec.x);
                    return;
                }

                if (Vec2(vec) - m_PrevDir == Vec2(0.0,0.0)) {
                    std::cerr << "Same coordinates. Moving on...\n";
                        return;
                }

                if (m_Waypoint.distance_between(vec) < 1.0f) {
                    if (m_WaypointsIter == m_Waypoints.end()) {
                        return;
                    }
                    m_Waypoint = *m_WaypointsIter++;
                }

                Vec2 nextVec = Vec2::utm_from_latlong(vec.y, vec.x) - m_PrevDir;
                Vec2 waypointVec = m_Waypoint - m_PrevDir;
                m_PrevDir = vec;
                std::cerr << "nextVec: " << nextVec.x << ',' << nextVec.y << '\n';
                std::cerr << "waypointVec: " << waypointVec.x << ',' << waypointVec.y << '\n';
                Gps ret;
                float steering = CalcSteering(nextVec, waypointVec);
                ret.steering = steering;
                ret.throttle = throttle;
                m_pGpsPublisher->publish(ret);
                m_PrevDir = vec;
            }

            float CalcSteering(const Vec2& currentDir, const Vec2& waypoint) {
                float angBetween = currentDir.angle_between(waypoint);
                std::cerr << "Angbetween: " << angBetween <<'\n';
                return k*std::tanh(angBetween);
            }
    };
}

int main(int argc, char** argv) {

    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<node::GpsNode>());
    rclcpp::shutdown();


}

