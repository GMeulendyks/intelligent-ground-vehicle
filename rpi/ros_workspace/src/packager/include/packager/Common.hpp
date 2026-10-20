#pragma once

namespace packager {

struct Vec3 {
    double x, y, z;
};

struct Vec2 {
    double x, y;
};

struct Polar2 {
    double m; // Magnitude
    double t; // Theta (angle, rad)
};

Polar2 Rec2Polar(Vec2 v);
Vec2 Polar2Rec(Polar2 p);
}; // namespace packager
