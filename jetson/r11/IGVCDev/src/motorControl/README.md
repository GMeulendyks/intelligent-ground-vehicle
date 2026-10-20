#Instructions
1. Flash the arduino with motorDrive.ino. This can be found in the arduino directory.
2. Set the DIP switches 1 - 6 on the motor driver to the following:
    * 111011
    * Please make note of the configuration prior to making adjustments. Take a picture!
2. Connect +5V, GND to the motor driver. Connect pin 11 to S1 of the driver.
3. ssh into the Raspberry Pi.
    * ssh littleblue@192.168.215.103
    * password: admin
    
    *note: thor-kauf247 is an authorized ssh client for the Raspberry Pi on LittleBlue so no password will be requseted*
4. Update the IGVCDev project repo.
5. Navigate to the constroller_ws directory.
6. Input the following commands:
    ```
    colcon build
    source install/setup.bash
    ros2 launch game_controller launch.py
    ```