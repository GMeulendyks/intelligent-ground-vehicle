# Table of Contents

[Introduction](#introduction)<br/>
[Components](#components)<br/>
&emsp;[Nvidia Jetson](#nvidia-jetson)<br/>
&emsp;[Docker Container ubuntu_ros2_iron:r11](#docker-container-ubuntu_ros2_iron:r11)<br/>
&emsp;[Docker Container ubuntu_ros2_iron:r6](#docker-container-ubuntu_ros2_iron:r6)<br/>
&emsp;[Raspberry PI](#raspberry-pi)<br/>

<br/>
<br/>

# Introduction

This folder contains pictures and documents explaining the layout of Little Blue.

<br/>
<br/>

# Components

## Nvidia Jetson

**Purpose:** The Nvidia Jetson is the main processor of Little Blue.

**Properties:**
| Property         | Value                 |
| :--------------- | :-------------------- |
| IP               | 192.168.215.200       |
| Netmask          | 255.255.255.0         |
| Model            | Orin Nano             |
| Operating System | Ubuntu 22.04.5 LTS    |
| Processor        | ARMv8 Processor rev 1 |
| RAM              | 8GB                   |

<br/>
<br/>

## Docker Container ubuntu_ros2_iron:r11

**Purpose:** Runs artifical intelligent and contains drivers for communication with the IMU, LIDAR, and GPS.

**Properties:**
| Property         | Value                 |
| :--------------- | :-------------------- |
| IP               | 192.168.215.200       |
| Netmask          | 255.255.255.0         |
| Model            | Orin Nano             |
| Operating System | Ubuntu 22.04.4 LTS    |
| Processor        | ARMv8 Processor rev 1 |
| RAM              | 8GB                   |

<br/>
<br/>

## Docker Container ubuntu_ros2_iron:r6

**Purpose:** Connects with cameras and contains the camera drivers.

**Properties:**
| Property         | Value                 |
| :--------------- | :-------------------- |
| IP               | 192.168.215.200       |
| Netmask          | 255.255.255.0         |
| Model            | Orin Nano             |
| Operating System | Ubuntu 22.04.4 LTS    |
| Processor        | ARMv8 Processor rev 1 |
| RAM              | 8GB                   |

<br/>
<br/>

## Raspberry PI

**Purpose:** The Raspberry PI is the main communicator with the motor driver and the Arduino R3.

**Properties:**
| Property         | Value                          |
| :--------------- | :----------------------------- |
| IP               | 192.168.215.201                |
| Netmask          | 255.255.255.0                  |
| Model            | Raspberry Pi 4 Model B         |
| Operating System | Ubuntu 22.04.3 LTS             |
| Processor        | Raspberry Pi 4 Model B Rev 1.4 |
| RAM              | 8GB                            |

<br/>
<br/>
