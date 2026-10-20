# About

Author: Duncan Clark  
Date: 10/15/2023  
Description: How to use these packages and built in packages  

This workspace is used to receive gamepad controller inputs. It is used as a testing ground to ensure I know how the information is transmitted in ROS.  

In reality, this code will never be used in release. This is because the control system should be receiving controller inputs, not a stand along controller node.  

## How to use a gamepad controller

There are many different versions of gamepad controllers on the market. ROS2 makes it easy to integrate all types of gamepad controllers regardless of brand. To test that your controller is working, follow the steps listed below:  

1. Plug your controller into your computer via USB
2. Start your ROS2 environment
3. Type the following command: ros2 run joy joy_node
    * This will start the built in joy_node which publishes your controller commands to the joy topic.
4. In a new terminal window, run the following command: ros2 topic echo /joy  
    * You should see the various controller inputs displayed in the terminal.  
  
If this does not work, try running the command ros2 run joy joy_enumerate_devices. This will list all the available controllers. If you do not see your controller, it may mean that ROS2 does not recognize it. Follow the standard procedures and ensuring your environment is configured properly and all software is up to date. 

## Connections for Arduino and Motor Driver

1. The Arduino should be connected to the Raspberry Pi via USB.
2. 5V and GND should be connected to the motor driver.
3. Pin 10 of the Arduino should be connected to S1 of the motor driver.
4. Pin 11 of the Arduino should be connected to S2 of the motor driver.
5. The DIP switches on the motor driver should have the following configuration from 1 - 6:
    * 011011

## Instructions for SSH into Raspberry Pi

1. Power Raspberry Pi. Ensure the device is connected to the network.
2. Go to the development computer and launch a terminal window. Type the following command:
    * ssh littleblue@192.168.215.103
    * The password isi "admin"
3. Navigate to the following directory:
    * ~/IGVCDev/Dev/RaspberryPi/controller_ws
4. Type the following commands:
    * colcon build
    * source install/setup.bash
    * ros2 launch game_controller launch.py

You should now be able to control the robot with the controller.