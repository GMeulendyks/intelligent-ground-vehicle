cmake_minimum_required(VERSION 3.8)
project(gps_hack)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
#find_package(odu_gps_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(gps_talker src/gps_talker.cpp)
set(UBLOX_LOCATION
    \"${CMAKE_INSTALL_PREFIX}/lib/${PROJECT_NAME}/ublox_processor\"
)
target_compile_definitions(gps_talker PUBLIC UBLOX_PROCESSOR=${UBLOX_LOCATION})
add_executable(s2s2s src/str2str2socket.c)
add_executable(ublox_processor src/ublox_processor.c)
ament_target_dependencies(gps_talker rclcpp std_msgs geometry_msgs)
target_link_libraries(gps_talker ${rclcpp_LIBRARIES})
install(TARGETS
  gps_talker
  DESTINATION lib/${PROJECT_NAME})

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(
    TARGETS
    gps_talker
    s2s2s
    ublox_processor
    DESTINATION
    lib/${PROJECT_NAME}
)
ament_package()
