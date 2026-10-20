from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node(
        #     package='joy',
        #     executable='joy_node',
        # ),
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            ros_arguments=[
                '--remap', '__ns:=/usb_cam_0',
                '--params-file', 'config/leftCamera.yaml'
            ]
        ),
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            ros_arguments=[
                '--remap', '__ns:=/usb_cam_1',
                '--params-file', 'config/rightCamera.yaml'
            ]
        ),
        Node(
            package='data',
            executable='talker'
        ),
        Node(
            package='data',
            executable='listener'
        )
    ])