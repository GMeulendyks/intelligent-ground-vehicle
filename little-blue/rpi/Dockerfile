
FROM ros:jazzy

# RUN apt-get install -y usbutils udev libusb-1.0-0 && apt-get clean

#Allow non-root users to access USB Devices
RUN usermod -aG dialout root && usermod -aG plugdev root

# Dependencies
RUN apt-get update && apt-get install -y build-essential curl gnupg2 \
    lsb-release wget sudo libusb-1.0-0-dev v4l-utils \
	python3 python3-pip libopencv-dev ros-jazzy-ament-cmake \
	ros-jazzy-usb-cam ros-jazzy-rviz2 vim nano emacs libreadline-dev

RUN apt-get update && apt-get install -y gstreamer1.0-tools gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-libav libopencv-dev ros-jazzy-nmea-msgs \
    ros-jazzy-mavros-msgs

COPY . usr/local/IGVCDev

SHELL ["/bin/bash", "-c"]

# ADD https://github.com/xsenssupport/Xsens_MTi_ROS_Driver_and_Ntrip_Client/tree/ros2 /usr/local/xsens_driver

RUN cd /usr/local && \
	git clone -b ros2 https://github.com/xsenssupport/Xsens_MTi_ROS_Driver_and_Ntrip_Client && \
	cp -r /usr/local/Xsens_*/src /usr/local/IGVCDev/ros_workspace/

RUN cd /usr/local/IGVCDev/ros_workspace/src && git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git

RUN cd /usr/local/IGVCDev/ros_workspace/src && git clone https://github.com/ros-drivers/usb_cam

RUN apt update && cd /usr/local/IGVCDev/ros_workspace && \
    . /opt/ros/jazzy/setup.bash && \
    rosdep install --from-paths src --ignore-src -r -y && \
    colcon build
