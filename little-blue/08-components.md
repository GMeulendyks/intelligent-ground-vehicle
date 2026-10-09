# Table of Contents

[Introduction](#introduction)<br/>
[Components](#components)<br/>
&emsp;[Nvidia Jetson](#nvidia-jetson)<br/>
&emsp;[Raspberry PI](#raspberry-pi)<br/>
&emsp;[Arduino](#arduino)<br/>
&emsp;[Cameras](#cameras)<br/>
&emsp;[GPS](#gps)<br/>
&emsp;[IMU](#imu)<br/>
&emsp;[Gamepad](#gamepad)<br/>
&emsp;[LIDAR](#lidar)<br/>
&emsp;[Network Hub](#network-hub)<br/>
&emsp;[Power Inverter](#power-inverter)<br/>
&emsp;[Motor Driver](#motor-driver)<br/>
&emsp;[DC Step Converter](#dc-step-converter)<br/>
&emsp;[Docker Container ubuntu_ros2_iron r11](#docker-container-ubuntu_ros2_iron-r11)<br/>
&emsp;[Docker Container ubuntu_ros2_iron r6](#docker-container-ubuntu_ros2_iron-r6)<br/>

<br/>
<br/>

# Introduction

This page contains documentation on each of Little Blue's components.

<br/>
<br/>

# Components

## Nvidia Jetson

**Purpose:** The Nvidia Jetson is the main processor of Little Blue. It handles a variety of tasks and is the main communication hub.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | Nvidia Orin Nano                                                                                                                               |
| Documentation      | [Available Here](https://dam-cdn.nvd.orangelogic.com/AssetLink/2ug686w80406gxf6q8uv7r3l7265m2n8.pdf)                                           |
| IP                 | 192.168.215.200                                                                                                                                |
| Netmask            | 255.255.255.0                                                                                                                                  |
| Operating System   | Ubuntu 22.04.5 LTS                                                                                                                             |
| Processor          | ARMv8 Processor rev 1                                                                                                                          |
| RAM                | 8GB                                                                                                                                            |

<br/>
<br/>

## Raspberry PI

**Purpose:** The Raspberry PI is the main communicator between the Nvidia Jetson and the Arduino.

**Properties:**
| Property           | Value                                                                                                                                                     |
| :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | Raspberry Pi 4 Model B                                                                                                                                    |
| Documentation      | [Available Here](https://pip-assets.raspberrypi.com/categories/545-raspberry-pi-4-model-b/documents/RP-008344-DS-7-raspberry-pi-4-product-brief.pdf)      |
| Schematics         | [Available Here](https://pip-assets.raspberrypi.com/categories/545-raspberry-pi-4-model-b/documents/RP-008345-DS-1-raspberry-pi-4-reduced-schematics.pdf) |
| IP                 | 192.168.215.201                                                                                                                                           |
| Netmask            | 255.255.255.0                                                                                                                                             |
| Operating System   | Ubuntu 22.04.3 LTS                                                                                                                                        |
| Processor          | Raspberry Pi 4 Model B Rev 1.4                                                                                                                            |
| RAM                | 8GB                                                                                                                                                       |

<br/>
<br/>

## Arduino

**Purpose:** The main communicator between the Raspberry PI and the motor driver.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | Arduino Uno R3                                                                                                                                 |
| Documentation      | [Available Here](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)                                                           |
| Software           | [Available Here](https://github.com/arduino-libraries/Servo)                                                                                   |
| Interfaces         | UART, I2C, SPI                                                                                                                                 |

<br/>
<br/>

## Cameras

**Purpose:** Gather 3D forward information for Little Blue to identify obstacles and position.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | a2A3840-45ucBAS                                                                                                                                |
| Documentation      | [Available Here](https://docs.baslerweb.com/a2a3840-45ucbas)                                                                                   |
| Software           | [Available Here](https://www.baslerweb.com/en/downloads/software/?downloadCategory.values.label.data=pylon&groupAssets.supportedOs.data=linux) |
| API                | [Available Here](https://docs.baslerweb.com/pylonapi/)                                                                                         |
| Resolution         | 3840px x 2160px                                                                                                                                |
| Frames Per Second  | 45                                                                                                                                             |
| Interfaces         | USB3                                                                                                                                           |

<br/>
<br/>

## GPS

**Purpose:** Gather top down information for Little Blue to identify obstacles and position.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | ZED-F9P-02B                                                                                                                                    |
| Data Sheet         | [Available Here](https://content.u-blox.com/sites/default/files/documents/ZED-F9P-02B_DataSheet_UBX-21023276.pdf)                              |
| Integration Manual | [Available Here](https://content.u-blox.com/sites/default/files/ZED-F9P_IntegrationManual_UBX-18010802.pdf)                                    |
| Interfaces         | UART, SPI, I2C, USB                                                                                                                            |

<br/>
<br/>

## IMU

**Purpose:** Gather force, angular velocity, and orientation information for Little Blue.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | MTi-600 DEV                                                                                                                                    |
| Documentation      | [Available Here](https://www.xsens.com/hubfs/Downloads/Manuals/MTi600-series_DK_Usermanual.pdf)                                                |
| Software           | [Available Here](https://base.xsens.com/s/article/MT-Manager-Installation-Guide-for-ubuntu-20-04-and-22-04?language=en_US)                     |
| Interfaces         | USB, CAN, RS232, RS422, UART                                                                                                                   |

<br/>
<br/>

## Gamepad

**Purpose:** Provide a manual input interface to Little Blue for movement and enabling autonomous mode.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | Logitech Wireless Gamepad F710                                                                                                                 |
| Documentation      | [Available Here](https://support.logi.com/hc/en-ca/articles/360023465553-Logitech-Wireless-Gamepad-F710-Technical-Specifications)              |
| Interfaces         | USB1.1 Nano 2.4GHz wireless                                                                                                                    |
| Range              | 10m/30ft                                                                                                                                       |

<br/>
<br/>

## LIDAR

**Purpose:** Determine distances from Little Blue to objects in a 360 degree radius.

**Properties:**
| Property           | Value                                                                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model              | RPLIDAR C1                                                                                                                                     |
| Documentation      | [Available Here](https://bucket-download.slamtec.com/9fd56b14eb46b11ffb38d861db4a7771c70e3095/SLAMTEC_rplidar_datasheet_C1_v1.2_en.pdf)        |
| Software           | [Available Here](https://github.com/Slamtec/rplidar_ros/tree/ros2)                                                                             |
| SDK Interface      | [Available Here](https://bucket-download.slamtec.com/6957283725b66750890024d1f0d12940fa079e06/LR002_SLAMTEC_rplidar_sdk_v2.0_en.pdf)           |
| Interfaces         | TTL UART                                                                                                                                       |
| Range              | 70% Reflectivity = 12m, 10% Reflectivity = 6m                                                                                                  |

<br/>
<br/>

## Network Hub

**Purpose:** A switchs that connect over ethernet.

**Properties:**
| Property            | Value                                                                                                                                          |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model               | GS308EP                                                                                                                                        |
| Datasheet           | [Available Here](https://www.downloads.netgear.com/files/GDC/GS305EP/GS305EP_GS305EPP_GS308EP_GS308EPP_GS316EP_GS316EPP_DS.pdf)                |
| Interfaces          | 8 Port RJ45 Gigabit Ethernet                                                                                                                   |
| Power Over Ethernet | Yes                                                                                                                                            |

<br/>
<br/>

## Power Inverter

**Purpose:** Changes DC current to AC current and provides it to Little Blue.

**Properties:**
| Property            | Value                                                                                                                                          |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model               | AIMS PWRI60012120S                                                                                                                             |
| Datasheet           | [Available Here](https://www.aimscorp.net/wp-content/uploads/2011/02/PWRI60012120S-022026.pdf)                                                 |
| Input               | 12V DC                                                                                                                                         |
| USB Output          | 5V DC                                                                                                                                          |

<br/>
<br/>

## Motor Driver

**Purpose:** The interface between the arduino and the motor.

**Properties:**
| Property            | Value                                                                                                                                          |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model               | Sabertooth 2x60                                                                                                                                |
| Documentation       | [Available Here](https://www.dimensionengineering.com/datasheets/Sabertooth2x60.pdf)                                                           |
| Interface           | RS-232 TTL 9600 Baud                                                                                                                           |
| Analog Input        | 0V-5V                                                                                                                                          |

<br/>
<br/>

## DC Step Converter

**Purpose:** Converts 24V input to 12V output.

**Properties:**
| Property            | Value                                                                                                                                          |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Model               | TOBSUN FA120                                                                                                                                   |
| Documentation       | TODO                                                                                                                                           |
| Input               | 24V Nominal                                                                                                                                    |
| Output              | 12V                                                                                                                                            |

<br/>
<br/>

## Docker Container ubuntu_ros2_iron r11

**Purpose:** Runs on the Nvidia Jetson and is responsible for artifical intelligent and contains drivers for communication with the IMU, LIDAR, and GPS.

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

## Docker Container ubuntu_ros2_iron r6

**Purpose:** Runs on the Nvidia Jetson and is responsible for connecting with cameras.

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
