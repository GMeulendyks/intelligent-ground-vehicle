#include "packager/Common.hpp"
#include <cmath>

namespace packager {

Polar2 Rec2Polar(Vec2 v) {
    return Polar2{std::sqrt(v.x * v.x + v.y * v.y), std::atan(v.y / v.x)};
}
Vec2 Polar2Rec(Polar2 p) {
    return Vec2{p.m * std::cos(p.t), p.m * std::sin(p.t)};
}
}; // namespace packager
