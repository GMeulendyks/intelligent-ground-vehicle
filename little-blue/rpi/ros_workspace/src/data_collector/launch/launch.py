from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='data_collector',
            executable='DataCollector',
            name='data_collector'
            ),
        ])


