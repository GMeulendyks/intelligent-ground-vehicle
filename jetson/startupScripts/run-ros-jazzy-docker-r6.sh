
# NOTE: this shellscript will start the docker but, at the present, is not connected
# to the volume
# add the mount below to mount the volume as the home directory for littleblue.
# You will need to copy the files in 
# littleblue-basler.tar.xz to the mounted volume
# without the volumne, any changes are lost when you exit the docker.

# if you want to save the image, find the running image with docker ps and run the
# command WHILE THE IMAGEW IS STILL RUNNING. Change the version number afte rthe colon
# so you don't overrite the existing image.

# docker container commit <container-id> ubuntu_ros2_jazzy:r<X>


Version=r6  # version created on Mar 6, 2026

# I think you need to use the nvidia-docker in order to access the GPUs
#nvidia-docker run \ # this was for previous versions
docker run \
	-ti --rm \
	--user=root \
	--privileged \
	--net=host -e DISPLAY=$DISPLAY \
	--ipc=host \
	-v /dev/bus/usb:/dev/bus/usb \
	-v /tmp/.X11-unix/:/tmp/.X11-unix \
	--mount source=littleblue-24.04,target=/home \
	ubuntu_ros2_jazzy:$Version /bin/bash



# insert the following above after the X11 option to mount the volume
#
