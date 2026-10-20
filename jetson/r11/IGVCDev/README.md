# About this Repo
Primary Author and Maintainer: Duncan Clark
Date: 10/9/2023

This branch was built around the following environment:
* Ubuntu 22.04
* Python 3.10
* ROS2 Iron
* Nvidia Jetson Nano for Little Blue
* Nvidia Jeston Xavier for Monarch 1

Any changes to the elements of this environment could render the source code incompatible. The following file outlines how to 
create this environment and ensure code compatibility. There are also instructions on how to execute the various packages 
included in this repository.


# SSH Keygen & Downloading Repository 

In order to download this code base and maintain it, you will want to set up a pair of SSH keys.
Use the following command in your terminal to generate a key pair:

`ssh-keygen -t rsa -b 2048` 

You can raise the size of the key, say to 4096, if you wish; 2048 is simply the minimum recommended size for rsa keys by gitlab. 
You will then be prompted to specify a file path, filename, and password for the keygen pair. Simply hit `enter` until the RSA keypair is generated. 
Next navigate to the newly generated ssh key pair and print the public ssh key to the screen

```
cd ~/.ssh
cat id_rsa.pub
```

Highlight the public ssh key pair from ssh-rsa to *user*@*computer*. Copy the highlighed public ssh key and navigate to the [gitlab repository](https://gitlab.com/belfore/IGVCDev)  
In the top left of the screen click on your profile icon then click edit profile. On the lefthand ribbon click *SSH Keys*. On the right side of the SSH Key tab click *Add new key*.

In the *Key* field paste your public ssh key. In the *title* field either leave default or name it appropriately. Lastly click *Add key*  
Your ssh key is now configured to your gitlab account. Doing this will allow you to easily interact with the codebase on gitlab.
Now you will need to clone the repository onto your computer, this can be done with the commands:


```
cd  ~

git clone git@gitlab.com:belfore/IGVCDev.git
``` 

This will download the repository to your home directory. The first time you do this you will prompted about the authenticity of the host, answer yes to the prompt. 
After the download finishes, you should have a copy of the repository on your computer in the directory where you invoked the clone command. Before you can
use any git commands to update the repository, you will need to configure a git username and user email.
This is done with the commands (if you have done this already previously skip this):

```
git config --global user.name "My Name"
git config --global user.email "My.Email@address.com"
```
If you use multiple git user names and email addresses, you can use `--local` instead of `--global` in
the IGVCDev directory to set them for only that repository.


# Environment Setup                              
### WORK IN PROGRESS   

# [Ubuntu 22.04](https://ubuntu.com/download/desktop "Link to download Ubuntu 22.04")                                             


Basic steps for booting Ubuntu 22.04:
* Download the iso file from the link above
* Download Win32DiskImager from [here](https://sourceforge.net/projects/win32diskimager/)
* Insert a flash drive into your computer and boot Win32DiskImager
* Load the iso file and select your flash drive from the Win32 options
* Once complete, remove flash drive and insert into the computer with which you want to install Ubuntu
* Follow the instructions laid out [here](https://ubuntu.com/tutorials/install-ubuntu-desktop#4-boot-from-usb-flash-drive)


# [CUDA and NVIDIA Drivers](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#introduction "Link to NVIDIA CUDA Installation guide for Linux")


There are multiple ways to install NVIDIA drivers onto an ubuntu system, but one of the
easiest ways that I have found has been to use a manual CUDA toolkit installation
through a .deb package. First, download the CUDA version you want from NVIDIA's website.
I chose to use [CUDA 10.2](https://developer.nvidia.com/cuda-10.2-download-archive "CUDA 10.2 download"),
as this is the version of CUDA that the JETSON is flashed with. However, you can use any version up
to 11.1 (currently the ZED SDK does not support version 11.2).  You will select your operating
system and architecture from the menus on this page, choose the deb(local) installer type. Open a
terminal and move to a convenient directory (I used downloads) and run the following commands:
```
get https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-ubuntu1604.pin
sudo mv cuda-ubuntu1604.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda-repo-ubuntu1604-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-10-2-local-10.2.89-440.33.01/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
```
These commands will retrieve the .deb packaging of the CUDA 10.2 toolkit, register it as a repository
with ubuntu, and then install the toolkit. The toolkit installation will also install the necessary
NVIDIA drivers, so that we do not have to worry about it. After we have installed the drivers
and toolkit, we now need to add it to the PATH variable. This is done with the:  
`export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}` command. Add this line to the end of your 
.bashrc configuration file location in the home directory (~). After adding this line, restart your PC
and the process should be finished.


# Packages to Install
* [ROS2 Iron](https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html "Link to ROS2 Iron installation instructions")
* Python 3.10 (Should be included with the Ubuntu 22.04 release)
* OpenCV for Python3 (sudo apt install python3-opencv)
* [OpenCV for C++](https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html "Installation instructions for C++ version of OpenCV")
* [PyTorch](https://pytorch.org/get-started/locally/ "Installation instructions for PyTorch")

# [ROS2 Iron](https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debians.html "Link to ROS2 Iron installation guide for Ubuntu")                                                                  


This ROS2 distrobution is fairly straight forward to install. Simply click the "ROS2 Iron" title above and follow the instructions.


# [ZED SDK](https://www.stereolabs.com/docs/installation/linux/ "ZED SDK Installation Guide")                     


In order to utilize the ZED2 Stereo Camera, we must install its Software Development Kit (SDK). The
downloads can be found [here](https://www.stereolabs.com/developers/release/ "ZED SDK Downloads"). Choose
the Ubuntu 16 installer for your version of CUDA. After downloading the installer, navigate to the
folder where you have it downloaded (typically the ~/Downloads folder) and give the installer
execution permissions: `chmod +x ZED_SDK_Ubuntu16_cuda10.2_v3.3.3.run` (the name of the .run file
may be different). Before running the installer, make sure to install and upgrade your version of
PIP for python3: `python3 -m pip install --upgrade pip` (you may have to run this command twice).
After adding execution permissions and updating PIP, run the installer:
`./ZED_SDK_Ubuntu16_cuda10.2_v3.3.3.run`. Read the license agreement, then hit q to exit it.
Several dependencies for the SDK might be missing on your system, the installer will ask you if you
want to install them, I recommend doing so; type y and enter to do so for each dependency. After
the installation is finished, restart your computer. You should now be able to run the SDK and its
features with the `ZED_Explorer` and other commands.






# [zed-ros-wrapper](https://github.com/stereolabs/zed-ros-wrapper " zed-ros-wrapper github link")


To install the zed-ros-wrapper, you simply need to clone the Git repository onto your computer, get
the necessary dependencies, and build the workspace. First I will cover setting up the wrapper in
its own workspace, then I will cover how you can integrate the wrapper with the existing codebase.


## Independent Workspace


Use the following commands in any convenient folder (the home folder, ~, works fine):
```
mkdir -p ~/catkin_ws/source
cd ~/catkin_ws/
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3
source devel/setup.bash
```
This will initialize your catkin_ws and set it up for use. Next, we need to clone the wrapper from
its repository, update dependencies, and build the workspace. This is accomplished with the following
commands:
```
cd ~/catkin_ws/src
git clone https://github.com/stereolabs/zed-ros-wrapper.git
cd ../
rosdep install --from-paths src --ignore-src -r -y
catkin_make -DCMAKE_BUILD_TYPE=Release
source ./devel/setup.bash
```


## Integrate wrapper into existing workspace TODO


The process to integrate the zed-ros-wrapper into our existing code base is not much different from
giving it its own workspace. The difference is that we will strip the wrapper of its git componenets
so that it can be properly included in our existing git repository. The commands are as follows:
```
cd ~
git clone https://github.com/stereolabs/zed-ros-wrapper.git
rsync -av --progress zed-ros-wrapper/ zed-ros-wrapper/src/zed-ros-wrapper --exclude .'git*'  (not quite correct yet TODO)
```
The rync command will copy the relevant parts of the wrapper, and discard the git portions of it,
removing the conflicts with our existing git configuration. The usage of the wrapper will be
covered in the next section.


# Running the ROS Applications TODO                           


After you have built and setup a catkin_ws, the packages that exist in that workspace can now be
executed in one of two ways, the `rosrun` command and with the use of launch files and the
`roslaunch` command.


*******************************************************************************
OBSOLETE - ZED2 network not running on Jetson.  
TODO  
Change AT_CHECK function to TORCH_CHECK function in the maskrcnn-benchmark
program. Change in maskrcnn-benchmark/csrc/cuda/. Change deform_conv_cuda.cu
and deform_pool_cuda.cu. Build fails on AT_CHECK with newer versions of pytorch
so this must be changed to successfully build the network.
