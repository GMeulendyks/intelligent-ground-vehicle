from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='joy',
            executable='joy_node',
            name='polling_gamepad'
            ),
        Node(
            package='arduino_control',
            executable='arduino_control',
            name='arduino_control'
            )
        ])

