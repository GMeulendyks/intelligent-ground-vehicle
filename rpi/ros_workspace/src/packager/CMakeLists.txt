cmake_minimum_required(VERSION 3.8)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
project(packager)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../cmake")
include(IGVCUtils)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(packager_msgs REQUIRED)
find_package(OpenCV REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_cmake_gtest REQUIRED)

  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
  add_subdirectory(test)

endif()

set(PROJECT_INCLUDE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

add_subdirectory("deps/yaml-cpp")
add_subdirectory("src")

add_library(PackagerLib OBJECT
    src/PackagerNode.cpp
    src/PackagerConfig.cpp
)

msg_targets(msgs packager_msgs)
set(PACKAGER_DEPS
    IGVCPackager 
    rclcpp::rclcpp 
    yaml-cpp
    ${msgs}
)

target_link_libraries(PackagerLib PUBLIC
    ${PACKAGER_DEPS}
)
target_include_directories(PackagerLib
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)


add_executable(PackagerNode 
    src/PackagerMain.cpp
)

target_include_directories(PackagerNode
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(
    PackagerNode 
    PRIVATE 
    PackagerLib
)

install(
    TARGETS
    PackagerNode
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
