---
sidebar_position: 21
title: Lab Setup Guide
---

# Lab Setup Guide

Complete guide for setting up your Physical AI development environment.

---

##  Quick Start

### Step 1: Install Ubuntu 22.04

**Download:** [Ubuntu 22.04 LTS](https://ubuntu.com/download/desktop)

**Installation Options:**
1. **Dual Boot** (Recommended) - Full performance
2. **Dedicated Machine** - Best option
3. **WSL2** - Limited GPU support

---

### Step 2: Install NVIDIA Drivers

```bash
# Check if NVIDIA GPU is detected
lspci | grep -i nvidia

# Add graphics-drivers PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install latest driver
sudo apt install nvidia-driver-535

# Reboot
sudo reboot

# Verify installation
nvidia-smi
```

Expected output:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.2   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
...
```

---

### Step 3: Install ROS 2 Humble

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Humble
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop

# Install development tools
sudo apt install python3-colcon-common-extensions
sudo apt install python3-rosdep
sudo rosdep init
rosdep update

# Add to bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**Verify:**
```bash
ros2 --version
# Should show: ros2 cli version 0.xx.x
```

---

### Step 4: Install Development Tools

```bash
# Python packages
sudo apt install python3-pip
pip3 install --upgrade pip

# Essential Python libraries
pip3 install opencv-python numpy matplotlib scipy
pip3 install torch torchvision  # For AI models

# Computer vision
sudo apt install ros-humble-cv-bridge
sudo apt install ros-humble-vision-opencv

# Development tools
sudo apt install git terminator
sudo apt install ros-humble-rqt*  # ROS tools

# Optional: VS Code
sudo snap install code --classic
```

---

### Step 5: Create ROS 2 Workspace

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Build workspace
colcon build

# Source workspace
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

##  Install Simulation Tools

### Gazebo Classic (Included with ROS 2 Humble)

```bash
# Already installed with ros-humble-desktop
# Verify
gazebo --version
```

### Gazebo Fortress (Optional - Newer Version)

```bash
sudo apt install ros-humble-ros-gz
```

---

##  Install Isaac Sim (Optional - Module 3)

**Requirements:**
- RTX GPU
- 50GB free disk space
- NVIDIA Omniverse account

**Steps:**

1. **Create Account:** [NVIDIA Developer](https://developer.nvidia.com/)

2. **Install Omniverse Launcher:**
```bash
# Download from: https://www.nvidia.com/en-us/omniverse/download/
# Run installer
chmod +x omniverse-launcher-linux.AppImage
./omniverse-launcher-linux.AppImage
```

3. **Install Isaac Sim via Launcher:**
   - Open Omniverse Launcher
   - Go to "Exchange" tab
   - Search "Isaac Sim"
   - Click "Install"
   - Choose Isaac Sim 2023.1.1 or later

4. **Verify Installation:**
```bash
# Launch Isaac Sim
~/.local/share/ov/pkg/isaac_sim-*/isaac-sim.sh
```

---

##  Test Your Setup

### Test 1: ROS 2 Communication

**Terminal 1:**
```bash
ros2 run demo_nodes_cpp talker
```

**Terminal 2:**
```bash
ros2 run demo_nodes_py listener
```

 You should see messages being published and received.

---

### Test 2: Gazebo Simulation

```bash
gazebo
```

 Gazebo window should open with empty world.

---

### Test 3: ROS 2 + Gazebo

```bash
# Install turtlebot3
sudo apt install ros-humble-turtlebot3*

# Set robot model
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc

# Launch simulation
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

 You should see TurtleBot3 in Gazebo.

---

### Test 4: Computer Vision

```python
# test_cv.py
import cv2
import numpy as np

# Create test image
img = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.putText(img, 'OpenCV Working!', (50, 240),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

cv2.imshow('Test', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

```bash
python3 test_cv.py
```

 Window with green text should appear.

---

##  Common Issues & Solutions

### Issue 1: NVIDIA Driver Not Working

**Symptoms:** `nvidia-smi` shows error

**Solution:**
```bash
# Remove old drivers
sudo apt purge nvidia-*
sudo apt autoremove

# Reinstall
sudo apt install nvidia-driver-535
sudo reboot
```

---

### Issue 2: ROS 2 Command Not Found

**Symptoms:** `ros2: command not found`

**Solution:**
```bash
source /opt/ros/humble/setup.bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

---

### Issue 3: Gazebo Black Screen

**Symptoms:** Gazebo opens but shows black screen

**Solution:**
```bash
# Update graphics drivers
sudo apt update
sudo apt upgrade

# Or use software rendering
export LIBGL_ALWAYS_SOFTWARE=1
gazebo
```

---

### Issue 4: Permission Denied

**Symptoms:** Permission errors when running ROS nodes

**Solution:**
```bash
# Add user to dialout group (for serial devices)
sudo usermod -a -G dialout $USER
sudo reboot
```

---

##  Recommended Directory Structure

```
~/
 ros2_ws/              # ROS 2 workspace
    src/              # Source code
    build/            # Build files
    install/          # Installed packages
    log/              # Build logs
 datasets/             # Training datasets
 models/               # ML models
 projects/             # Course projects
```

---

##  Essential Tools

### Terminal Multiplexer: Terminator

```bash
sudo apt install terminator

# Launch
terminator
```

**Shortcuts:**
- `Ctrl+Shift+E` - Split vertical
- `Ctrl+Shift+O` - Split horizontal
- `Ctrl+Shift+W` - Close pane

---

### ROS Tools

```bash
# Node graph visualization
rqt_graph

# Topic monitor
rqt_topic

# Service caller
rqt_service_caller

# All-in-one
rqt
```

---

### VS Code Extensions

1. **ROS** - Official ROS extension
2. **Python** - Python IntelliSense
3. **C/C++** - For C++ nodes
4. **CMake** - CMake support
5. **URDF** - URDF syntax highlighting

---

##  Optional: Jetson Setup (Edge Deployment)

### Flash Jetson Orin Nano

1. **Download JetPack:** [NVIDIA JetPack](https://developer.nvidia.com/jetpack)

2. **Flash SD Card:**
```bash
# Use balenaEtcher or NVIDIA SDK Manager
```

3. **First Boot Setup:**
```bash
# Update system
sudo apt update
sudo apt upgrade

# Install ROS 2
# Follow same steps as Ubuntu setup
```

4. **Install Isaac ROS (on Jetson):**
```bash
# Clone Isaac ROS
cd ~/ros2_ws/src
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git

# Build
cd ~/ros2_ws
colcon build
```

---

##  Next Steps

 Hardware installed and verified
 ROS 2 working
 Simulation tools ready

**Now you're ready to start the course!**

**[Begin Module 1: ROS 2 →](./module-01-ros2/chapter-01-ros2-architecture)**

---

##  Need Help?

- **Hardware issues:** Check [Hardware Requirements](./hardware-requirements)
- **Software issues:** Ask the chatbot
- **ROS 2 issues:** [ROS 2 Documentation](https://docs.ros.org/en/humble/)

---

**Pro Tip:** Keep a backup of your working setup using Timeshift or Clonezilla!
