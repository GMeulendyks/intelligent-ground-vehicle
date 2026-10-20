add_library(providers OBJECT
    ImageProvider.cpp
    IMUProvider.cpp
    LidarProvider.cpp
    MotorControlProvider.cpp
)
target_include_directories(providers PRIVATE ${INCLUDE})
target_link_libraries(
    providers 
    PUBLIC 
    ${OpenCV_LIBS}
    rclcpp::rclcpp
    ${sensor_msgs_TARGETS}
    ${packager_msgs_TARGETS}
)
