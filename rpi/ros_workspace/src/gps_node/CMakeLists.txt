cmake_minimum_required(VERSION 3.8)
project(gps_node)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../cmake")
include(IGVCUtils)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(packager_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(GeographicLib REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()


add_executable(gps_node src/NodeMain.cpp)

msg_targets(msgs packager_msgs)
target_include_directories(gps_node PUBLIC
    ${GeographicLib_INCLUDE_DIRS}
)
target_link_libraries(gps_node
    PUBLIC
    rclcpp::rclcpp
    ${GeographicLib_LIBRARIES}
    ${msgs}
)

install(
    TARGETS
    gps_node
    DESTINATION
    lib/${PROJECT_NAME}
)



ament_package()
