cmake_minimum_required(VERSION 3.8)
project(data_collector)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../cmake")
include(IGVCUtils)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-fexperimental-library)
endif()

set(CXX_STANDARD 20)
set(CXX_STANDARD_REQUIRED ON)


# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(packager_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(OpenCV REQUIRED)
find_package(utils REQUIRED)

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

add_executable(DataCollector src/DataCollector.cpp)

msg_targets(msgs packager_msgs sensor_msgs)

#add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../../utils/cpp ${CMAKE_BINARY_DIR}/utils)

target_link_libraries(DataCollector
    PRIVATE
    ${OpenCV_LIBS}
    rclcpp::rclcpp
    utils::IGVCUtils
    ${msgs}
)

install(
    TARGETS
    DataCollector
    DESTINATION
    lib/${PROJECT_NAME}
)
install(
    DIRECTORY
    launch
    DESTINATION
    share/${PROJECT_NAME}
)

ament_package()
