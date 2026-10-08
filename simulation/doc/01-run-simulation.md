# Manual Simulation Operation

This guide explains how to launch and manually operate the Intelligent Ground Vehicle (IGV) simulation. The simulation uses three terminals to run the Gazebo simulation, RViz, and keyboard controls.

## 1. Navigate to the ROS 2 Workspace

Open a terminal and navigate to the ROS 2 workspace:

```bash
cd ~/intelligent-ground-vehicle/simulation/gazebo_classic_ros2_ws/ros2_ws
```

Build the workspace:

```bash
rosdep install -i --from-path src --rosdistro iron -y
```

```bash
colcon build --symlink-install
```

Source ROS 2 Iron and the workspace:

```bash
source /opt/ros/iron/setup.bash
```
```bash
source install/setup.bash
```

These commands must be run in each new terminal used for the simulation.

## 2. Launch the Simulation

In the first terminal, launch the small course simulation:

```bash
ros2 launch skid_steer_robot small_course.launch.py
```

This launches the simulated skid-steer robot and the Gazebo environment.

Keep this terminal running while operating the simulation.

## 3. Launch RViz

Open a second terminal and navigate to the ROS 2 workspace:

```bash
cd ~/intelligent-ground-vehicle/simulation/gazebo_classic_ros2_ws/ros2_ws
```

Source ROS 2 and the workspace:

```bash
source /opt/ros/iron/setup.bash
```
```bash
source install/setup.bash
```

Launch RViz:

```bash
rviz2 -d src/skid_steer_robot/config/robot_config.rviz
```

RViz provides a visualization of the robot and ROS data while the simulation is running.

## 4. Start Manual Keyboard Control

Open a third terminal and navigate to the ROS 2 workspace:

```bash
cd ~/intelligent-ground-vehicle/simulation/gazebo_classic_ros2_ws/ros2_ws
```

Source ROS 2 and the workspace:

```bash
source /opt/ros/iron/setup.bash
```
```bash
source install/setup.bash
```

Start the keyboard controller:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Keep this terminal selected while controlling the vehicle. The movement commands are sent immediately when a key is pressed and do not require Enter.

## 5. Movement Controls

The keyboard layout used to control the vehicle is:

```text
   u    i    o
   j    k    l
   m    ,    .
```

| Key | Action |
| --- | --- |
| `i` | Move forward |
| `,` | Move backward |
| `j` | Turn left |
| `l` | Turn right |
| `k` | Stop |
| `u` | Move forward and turn left |
| `o` | Move forward and turn right |
| `m` | Move backward and turn left |
| `.` | Move backward and turn right |

## 6. Speed Controls

The speed of the simulated vehicle can be adjusted while the keyboard controller is running.

| Key | Action |
| --- | --- |
| `q` | Increase linear and angular speed by 10% |
| `z` | Decrease linear and angular speed by 10% |
| `w` | Increase linear speed by 10% |
| `x` | Decrease linear speed by 10% |
| `e` | Increase angular speed by 10% |
| `c` | Decrease angular speed by 10% |

The current linear and angular speed values are displayed in the `teleop_twist_keyboard` terminal.

## 7. Stopping the Simulation

To stop a running ROS process, select its terminal and press:

```text
Ctrl+C
```

Stop the keyboard controller, RViz, and Gazebo when finished with the simulation.
