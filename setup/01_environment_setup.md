# Environment Setup

1. Setup a Ubuntu 22.04 environment.
	1. I recommend an oracle VM. You can download virtualbox here: https://www.virtualbox.org/wiki/Downloads
	2. You can download Ubuntu 22.04.5 .iso from here: https://www.releases.ubuntu.com/22.04/
	3. I recommend roughly:
		1. 50GB-100GB disk space
		2. 8-16GB of RAM
		3. 2-4 processors


2. Update Ubuntu packages:
```bash
sudo apt update && sudo apt upgrade
```


3. Prepare to install ROS Iron. Follow this guide https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debs.html
```bash
sudo apt install software-properties-common

sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
```


4. Install all the packages you're going to need (grab a coffee, this will take a while):
```bash
sudo apt install -y \
  git \
  ros-iron-desktop \
  ros-iron-ros-gz \
  ros-iron-xacro \
  ros-iron-robot-state-publisher \
  ros-iron-joint-state-publisher \
  ros-iron-teleop-twist-keyboard \
  ros-iron-rviz2 \
  ros-iron-gazebo-ros-pkgs \
  ros-iron-mavros-msgs \
  ros-iron-nmea-msgs \
  ros-iron-asio-cmake-module \
  ros-iron-diagnostic-updater \
  ros-iron-pcl-ros \
  ros-iron-robot-localization \
  xterm \
  python3 \
  python3-colcon-common-extensions \
  python3-rosdep \
  docker \
  docker-cli \
  clang \
  libasio-dev
```


5. Prepare some of the packages after installation.
```bash
sudo rosdep init
```
```bash
rosdep update
```
```bash
git config --global user.email "you@example.com"
```
```bash
git config --global user.name "Your Name"
```


6. Install pylon 26.02. This is already in the repo, but can also be downloaded from [here](https://www.baslerweb.com/en/downloads/software/?downloadCategory.values.label.data=pylon&groupAssets.supportedOs.data=linux)
```bash
tar -xvzf pylon-26.02.1_linux-x86_64_debs.tar.gz
```
```bash
sudo apt install pylon-26.02.1_linux-x86_64_debs/pylon_26.02.1-deb0_amd64.deb
```


7. Create a new github ssh key
	1. Folow this guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
```bash
ssh-keygen -t ed25519 -C "YOUR_EMAIL@example.com"

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/id_ed25519 # Or whatever you named the file.
```


8. Add the public ssh key to your github
	1. Follow this guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?tool=webui
```bash
# Copy and paste this into your GitHub account ssh keys.
cat ~/.ssh/id_ed25519.pub
```


9. Clone this repository
	1. NOTE: Run this in a folder of your choice
```bash
git clone git@github.com:GMeulendyks/intelligent-ground-vehicle.git
```


10. Change permissions on the scripts so they can run.

```bash
chmod +700 build
```

```bash
chmod +700 clean
```

```bash
chmod +700 run
```

```bash
chmod +700 update
```
