
# docker buildx build --platform linux/aarch64 --output type=local,dest=. .

# This is the current version of the rpi
FROM --platform=$BUILDPLATFORM ubuntu:22.04 AS rpibuilder

SHELL ["/bin/bash", "-c"]

WORKDIR /home/root

RUN apt update

# Install the ROS keyring to allow us to install ROS packages.
RUN apt install -y software-properties-common && \
    add-apt-repository universe && \
    apt update && \
    apt install curl -y && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt update

# Set time zone to not be asked during ROS installation.
RUN apt install -y tzdata && \
    cp /usr/share/zoneinfo/America/Virgin /etc/localtime

# Install ROS dependencies
RUN apt install -y \
    build-essential \
    libopencv-dev \
    libgeographic-dev \
    ros-iron-ros-base \
    ros-iron-geographic-msgs \
    python3-colcon-common-extensions

# Copy the code and prepare for building.
COPY . /home/root
RUN cd /home/root/ros_workspace

# Build
RUN source /opt/ros/iron/setup.bash && \
    colcon build --symlink-install

# Copy artifacts to local machine
FROM scratch
COPY --from=rpibuilder /home/root/build /build
COPY --from=rpibuilder /home/root/install /install
COPY --from=rpibuilder /home/root/log /log
