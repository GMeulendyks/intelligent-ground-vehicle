#!/bin/bash

source /opt/ros/iron/setup.bash

cd /home/$USER/IGVCDev/src/motorControl/rpi/controller_ws

git switch master

git fetch 

git pull

colcon build

source install/setup.bash

ros2 launch game_controller launch.py

