add_library(nodes INTERFACE
    GenericNode.hpp
)

target_link_libraries(nodes
    INTERFACE
    providers
    rclcpp::rclcpp
    ${sensor_msgs_TARGETS}
)

target_include_directories(nodes
    INTERFACE
    ${INCLUDE}
)
