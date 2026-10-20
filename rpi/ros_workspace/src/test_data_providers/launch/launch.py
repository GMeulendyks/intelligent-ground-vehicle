from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='test_data_providers',
            executable='Cam0NodeMain',
            name='Cam0'
            ),
        Node(
            package='test_data_providers',
            executable='Cam1NodeMain',
            name='Cam1'
            ),
        Node(
            package='test_data_providers',
            executable='LidarNodeMain',
            name='Lidar'
            ),
        Node(
            package='test_data_providers',
            executable='ImuNodeMain',
            name='Imu'
            ),
#        Node(
#            package='test_data_providers',
#            executable='MotorControlNodeMain',
#            name='MotorControl'
#            )
        ])


