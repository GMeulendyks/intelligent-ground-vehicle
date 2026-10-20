
echo NOTE: Need to set dev links for rplider, xsens, and ublox in the container
Version=r11
#nvidia-docker run \
docker run \
	-ti --rm \
	--user=root \
	--privileged \
	--net=host -e DISPLAY=:1 \
	-v /dev/bus/usb:/dev/bus/usb \
	-v /tmp/.X11-unix/:/tmp/.X11-unix --mount source=home,target=/home \
	ubuntu_ros2_iron:$Version /bin/bash
