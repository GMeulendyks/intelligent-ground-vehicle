# Instructions

This package is used for data collection of the robot. It launches all nodes necessary to do data collection. If some nodes are not required, you can remove them from the launch file found at /data_collection/ws/install/data/share/data/launch.py.

1. Navigate to "data_collection_ws"
2. Type the command: source install/setup.bash
3. Type the command: ros2 launch data launch.py

This will launch 2 cameras and the controller node. 

## Notes

1. All nodes are launched, but data collection doesn't start until the "start" button is pressed on the controller.
2. The left camera must be plugged into the KV260 first for configuration purposes. Than the right camera can be plugged in. 