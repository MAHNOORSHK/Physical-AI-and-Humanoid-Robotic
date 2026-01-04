---
sidebar_position: 1
title: Chapter 1 - ROS 2 Architecture
---

# Chapter 1: Introduction to ROS 2 Architecture

**⏱ Week 3, Days 1-2** | ** Module 1: The Robotic Nervous System**

---

##  Learning Objectives

By the end of this chapter, you will:

-  Understand the evolution from ROS 1 to ROS 2
-  Explain the DDS middleware and its benefits
-  Identify ROS 2 core concepts: nodes, topics, services, actions
-  Set up ROS 2 Humble development environment
-  Create and run your first ROS 2 node

---

##  What is ROS 2?

**ROS 2 (Robot Operating System 2)** is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

### Why "Operating System"?

ROS 2 is not a traditional operating system like Windows or Linux. Instead, it's a **middleware framework** that provides:

- **Communication infrastructure** between robot components
- **Hardware abstraction** layer
- **Package management** system
- **Build system** and development tools
- **Common robotics libraries** and algorithms

Think of ROS 2 as the **nervous system** of a robot, enabling different parts to communicate and coordinate.

---

##  ROS 1 vs ROS 2: The Evolution

### Why ROS 2?

ROS 1 was revolutionary but had limitations for production robotics:

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| **Real-time** | Not supported | Real-time capable |
| **Security** | None | DDS security |
| **Platforms** | Linux only | Linux, Windows, macOS |
| **Communication** | Custom TCPROS | DDS standard |
| **Single Point of Failure** | Master node required | Fully distributed |
| **Multi-robot** | Difficult | Native support |
| **Production-ready** | Research-focused | Industry-grade |

### Key Improvements in ROS 2

1. **No Master Node** - Fully distributed architecture
2. **DDS Middleware** - Industry-standard communication
3. **Real-time Support** - For safety-critical applications
4. **Better Python 3 Support** - Modern language features
5. **Improved Build System** - Ament/Colcon instead of Catkin
6. **Quality of Service (QoS)** - Reliable communication policies

---

##  ROS 2 Architecture

### The Big Picture

```

                  Application Layer                   
          (Your Robot Code - Python/C++)             

                    

                  ROS 2 Client Libraries              
              (rclpy, rclcpp, rclnodejs)             

                    

                    rcl (ROS Client)                  
           (Core ROS functionality in C)             

                    

                  DDS Middleware                      
        (FastDDS, CycloneDDS, RTI Connext)          

                    

                     Network                          
              (UDP/TCP Transport)                     

```

### DDS Middleware Layer

**DDS (Data Distribution Service)** is an industry-standard middleware for real-time systems.

**Benefits:**
- **Peer-to-peer communication** - No central broker
- **Automatic discovery** - Nodes find each other
- **Quality of Service** - Reliability guarantees
- **Real-time capable** - Predictable latency
- **Security** - Built-in authentication and encryption

**Available DDS Implementations:**
- **FastDDS** (Default in ROS 2 Humble)
- **CycloneDDS** (Lightweight alternative)
- **RTI Connext** (Commercial, high-performance)

---

##  Core Concepts

### 1. Nodes

A **node** is an executable that uses ROS to communicate with other nodes.

**Characteristics:**
- Single purpose (sensor reading, motor control, etc.)
- Can be written in Python, C++, or other languages
- Communicate via topics, services, and actions
- Run independently and can be distributed

**Example:** A camera node publishes images, while a vision node processes them.

### 2. Topics (Publish-Subscribe)

**Topics** enable asynchronous, one-to-many communication.

- **Publisher** sends messages to a topic
- **Subscriber** receives messages from a topic
- Many-to-many relationships possible

**Use case:** Streaming sensor data (camera, LiDAR, IMU)

### 3. Services (Request-Response)

**Services** provide synchronous, one-to-one communication.

- **Client** sends a request
- **Server** processes and returns a response

**Use case:** Configuration changes, one-time queries

### 4. Actions (Goal-Feedback-Result)

**Actions** are for long-running tasks with feedback.

- **Client** sends a goal
- **Server** provides periodic feedback
- **Result** returned when complete
- Can be canceled or preempted

**Use case:** Navigation, manipulation tasks

---

##  Installation & Setup

### System Requirements

- **OS:** Ubuntu 22.04 (Jammy Jellyfish)
- **ROS 2 Version:** Humble Hawksbill (LTS until 2027)
- **Python:** 3.10+
- **Disk Space:** 5GB minimum

### Installation Steps

#### Step 1: Set Locale

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

#### Step 2: Add ROS 2 Repository

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

#### Step 3: Install ROS 2 Humble

```bash
sudo apt update
sudo apt upgrade

# Desktop install (Recommended)
sudo apt install ros-humble-desktop

# Or minimal install
# sudo apt install ros-humble-ros-base
```

#### Step 4: Setup Environment

```bash
# Add to ~/.bashrc for automatic sourcing
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Verify installation
ros2 --version
```

#### Step 5: Install Development Tools

```bash
sudo apt install python3-colcon-common-extensions
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

### Testing Your Installation

```bash
# Terminal 1: Run talker
ros2 run demo_nodes_cpp talker

# Terminal 2: Run listener
ros2 run demo_nodes_py listener
```

You should see the talker publishing messages and the listener receiving them!

---

##  Your First ROS 2 Node

Let's create a simple "Hello World" node in Python.

### Step 1: Create Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### Step 2: Create Package

```bash
ros2 pkg create --build-type ament_python --node-name hello_world my_first_package
cd ~/ros2_ws
```

### Step 3: Write the Node

Edit `~/ros2_ws/src/my_first_package/my_first_package/hello_world.py`:

```python
import rclpy
from rclpy.node import Node

class HelloWorldNode(Node):
    def __init__(self):
        super().__init__('hello_world')
        self.get_logger().info('Hello from ROS 2! ')

        # Create a timer that calls our callback every second
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f'Message #{self.counter}: Hello World!')

def main(args=None):
    rclpy.init(args=args)
    node = HelloWorldNode()
    rclpy.spin(node)

    # Cleanup
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Step 4: Build and Run

```bash
cd ~/ros2_ws
colcon build --packages-select my_first_package

# Source the workspace
source install/setup.bash

# Run the node
ros2 run my_first_package hello_world
```

**Expected Output:**
```
[INFO] [hello_world]: Hello from ROS 2! 
[INFO] [hello_world]: Message #1: Hello World!
[INFO] [hello_world]: Message #2: Hello World!
[INFO] [hello_world]: Message #3: Hello World!
...
```

---

##  Understanding the Code

### Key Components

```python
import rclpy                    # ROS 2 Python library
from rclpy.node import Node     # Node base class
```

**rclpy** is the ROS 2 Python client library. It provides all the functionality to create nodes, publish/subscribe, etc.

```python
class HelloWorldNode(Node):
    def __init__(self):
        super().__init__('hello_world')  # Node name
```

Every node must inherit from the `Node` class and call `super().__init__()` with a unique node name.

```python
self.timer = self.create_timer(1.0, self.timer_callback)
```

Creates a timer that calls `timer_callback()` every 1.0 seconds.

```python
rclpy.init(args=args)    # Initialize ROS 2
node = HelloWorldNode()   # Create node instance
rclpy.spin(node)         # Keep node running
```

**rclpy.spin()** keeps the node alive and processes callbacks until interrupted (Ctrl+C).

---

##  ROS 2 Command-Line Tools

### Essential Commands

```bash
# List all nodes
ros2 node list

# Get info about a node
ros2 node info /hello_world

# List all topics
ros2 topic list

# Echo messages from a topic
ros2 topic echo /my_topic

# List all services
ros2 service list

# Call a service
ros2 service call /my_service std_srvs/srv/Trigger

# View package contents
ros2 pkg list
ros2 pkg executables my_first_package

# Run a node
ros2 run <package_name> <executable_name>

# Launch multiple nodes
ros2 launch <package_name> <launch_file>
```

---

##  Hands-On Lab

### Lab 1: Explore TurtleSim

TurtleSim is a simple simulator for learning ROS 2.

**Terminal 1: Run TurtleSim**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2: Control with Keyboard**
```bash
ros2 run turtlesim turtle_teleop_key
```

**Terminal 3: Inspect**
```bash
# List nodes
ros2 node list

# List topics
ros2 topic list

# Echo turtle pose
ros2 topic echo /turtle1/pose

# Inspect topic info
ros2 topic info /turtle1/cmd_vel

# View message interface
ros2 interface show geometry_msgs/msg/Twist
```

### Lab 2: Modify Your First Node

**Challenge:** Modify the `hello_world.py` node to:
1. Accept a parameter for the timer frequency
2. Change the message to include a custom greeting
3. Add a counter that prints how many times it has run

**Hint:** Use `self.declare_parameter()` and `self.get_parameter()`.

---

##  Key Takeaways

 ROS 2 is a middleware framework for robot communication
 DDS provides reliable, real-time, distributed communication
 Nodes are independent processes that communicate via topics/services/actions
 rclpy is the Python client library for ROS 2
 Use command-line tools to inspect and debug ROS 2 systems

---

##  Additional Resources

- [ROS 2 Official Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [DDS Specification](https://www.omg.org/spec/DDS/)
- [ROS 2 Design](https://design.ros2.org/)

---

##  Next Chapter

Ready to dive deeper into ROS 2 communication?

**[Chapter 2: Topics, Services, and Actions →](./chapter-02-topics-services-actions)**

Learn how nodes communicate with each other using topics (streaming data), services (request-response), and actions (long-running tasks).

---

** Questions?** Use the chatbot widget to ask about anything in this chapter!
