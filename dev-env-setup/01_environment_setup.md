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
3. Prepare to install ROS Iron
	1. Follow this guide: https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debs.html
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
  xterm \
  python3 \
  python3-colcon-common-extensions \
  python3-rosdep \
  docker \
  docker-cli \
  clang
```
5. Prepare some of the packages after installation.
```bash
sudo rosdep init

rosdep update

git config --global user.email "you@example.com"

git config --global user.name "Your Name"
```
5. Create a new github ssh key
	1. Folow this guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
```bash
ssh-keygen -t ed25519 -C "YOUR_EMAIL@example.com"

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/id_ed25519 # Or whatever you named the file.
```
6. Add the public ssh key to your github
	1. Follow this guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?tool=webui
```bash
# Copy and paste this into your GitHub account ssh keys.
cat ~/.ssh/id_ed25519.pub
```
7. Clone this repository
	1. NOTE: Run this in a folder of your choice
```bash
git clone git@github.com:GMeulendyks/intelligent-ground-vehicle.git
```
