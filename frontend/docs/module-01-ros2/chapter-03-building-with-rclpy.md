---
sidebar_position: 3
title: Chapter 3 - Building with rclpy
---

# Chapter 3: Building Robot Systems with rclpy

**⏱ Week 4-5** | ** Module 1: The Robotic Nervous System**

---

##  Learning Objectives

-  Integrate Python AI/ML code with ROS 2 using rclpy
-  Implement robot control loops and state machines
-  Handle parameters and dynamic reconfiguration
-  Create launch files for multi-node systems
-  Understand URDF for robot description

---

##  Integrating AI with ROS 2

### Computer Vision Pipeline

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection')

        # Bridge to convert ROS Image to OpenCV
        self.bridge = CvBridge()

        # Subscribe to camera
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publish velocity commands
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Object detection node started')

    def image_callback(self, msg):
        # Convert ROS Image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # Detect objects
        detections = self.detect_objects(cv_image)

        # Make decision
        command = self.compute_control(detections)

        # Publish command
        self.cmd_vel_pub.publish(command)

    def detect_objects(self, image):
        # Simple color-based detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Detect red objects
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return {'detected': True, 'cx': cx, 'cy': cy}

        return {'detected': False}

    def compute_control(self, detections):
        twist = Twist()

        if detections['detected']:
            image_center = 320
            error = detections['cx'] - image_center

            # Proportional controller
            twist.angular.z = -error * 0.002
            twist.linear.x = 0.2

            self.get_logger().info(f'Tracking object, error: {error}')
        else:
            # Stop if no object
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        return twist

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

---

### Using TensorFlow/PyTorch

```python
import torch
from torchvision import models, transforms

class AIVisionNode(Node):
    def __init__(self):
        super().__init__('ai_vision')

        # Load pre-trained model
        self.model = models.resnet50(pretrained=True)
        self.model.eval()

        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.classify_image,
            10
        )

    def classify_image(self, msg):
        # Convert to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # Preprocess
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        input_tensor = self.transform(rgb_image)
        input_batch = input_tensor.unsqueeze(0)

        # Inference
        with torch.no_grad():
            output = self.model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            class_id = torch.argmax(probabilities).item()

        self.get_logger().info(f'Detected class: {class_id}')
```

---

##  Parameters

Parameters allow dynamic configuration without restarting nodes.

```python
class ConfigurableNode(Node):
    def __init__(self):
        super().__init__('configurable_node')

        # Declare parameters with defaults
        self.declare_parameter('max_speed', 1.0)
        self.declare_parameter('detection_threshold', 0.5)
        self.declare_parameter('camera_topic', '/camera/image_raw')

        # Get parameter values
        self.max_speed = self.get_parameter('max_speed').value
        self.threshold = self.get_parameter('detection_threshold').value
        self.camera_topic = self.get_parameter('camera_topic').value

        self.get_logger().info(f'Max speed: {self.max_speed}')
        self.get_logger().info(f'Threshold: {self.threshold}')

        # Parameter callback for dynamic updates
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'max_speed':
                self.max_speed = param.value
                self.get_logger().info(f'Updated max_speed: {param.value}')

        return rclpy.parameter.SetParametersResult(successful=True)
```

**Set parameter from command line:**
```bash
ros2 param set /configurable_node max_speed 2.0
ros2 param get /configurable_node max_speed
ros2 param list /configurable_node
```

---

##  Launch Files

Launch files start multiple nodes with configuration.

**File:** `robot_launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='camera_node',
            name='camera',
            parameters=[{
                'frame_rate': 30,
                'resolution': '640x480'
            }]
        ),
        Node(
            package='my_package',
            executable='object_detection',
            name='detector',
            parameters=[{
                'detection_threshold': 0.7
            }],
            remappings=[
                ('/camera/image_raw', '/usb_cam/image_raw')
            ]
        ),
        Node(
            package='my_package',
            executable='controller',
            name='robot_controller',
            parameters=[{
                'max_speed': 1.5
            }]
        )
    ])
```

**Run launch file:**
```bash
ros2 launch my_package robot_launch.py
```

---

##  URDF - Robot Description

URDF (Unified Robot Description Format) describes robot structure.

### Simple Humanoid URDF

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Base Link (Pelvis) -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.15"/>
      </geometry>
      <material name="grey">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.15"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0"
               iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.25 0.15 0.4"/>
      </geometry>
      <material name="blue">
        <color rgba="0.0 0.0 0.8 1.0"/>
      </material>
    </visual>
    <inertial>
      <mass value="8.0"/>
      <inertia ixx="0.08" ixy="0" ixz="0"
               iyy="0.08" iyz="0" izz="0.08"/>
    </inertial>
  </link>

  <!-- Joint: Base to Torso -->
  <joint name="base_to_torso" type="revolute">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1.0"/>
  </joint>

  <!-- Right Arm -->
  <link name="right_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
    </visual>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="shoulder_right" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="0.15 -0.1 0.35" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="50" velocity="2.0"/>
  </joint>

</robot>
```

---

### Visualizing URDF

```bash
# Install joint-state-publisher-gui
sudo apt install ros-humble-joint-state-publisher-gui

# Visualize in RViz
ros2 run joint_state_publisher_gui joint_state_publisher_gui --ros-args -p robot_description:="$(cat robot.urdf)"

ros2 run rviz2 rviz2
```

---

##  Complete Example: Object Tracking Robot

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class ObjectTrackingRobot(Node):
    def __init__(self):
        super().__init__('object_tracker')

        # Parameters
        self.declare_parameter('max_speed', 0.5)
        self.declare_parameter('kp', 0.002)  # Proportional gain

        self.max_speed = self.get_parameter('max_speed').value
        self.kp = self.get_parameter('kp').value

        # CV Bridge
        self.bridge = CvBridge()

        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.debug_image_pub = self.create_publisher(Image, '/debug_image', 10)

        # State
        self.target_detected = False
        self.target_x = 0

        self.get_logger().info('Object tracking robot initialized')

    def image_callback(self, msg):
        # Convert to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # Detect target
        detected, target_x = self.detect_target(cv_image)

        # Control
        if detected:
            self.track_target(target_x, cv_image.shape[1])
        else:
            self.search_for_target()

        # Publish debug image
        debug_msg = self.bridge.cv2_to_imgmsg(cv_image, 'bgr8')
        self.debug_image_pub.publish(debug_msg)

    def detect_target(self, image):
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Red color detection
        lower = np.array([0, 100, 100])
        upper = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > 500:  # Minimum area threshold
                M = cv2.moments(largest)
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # Draw circle on target
                    cv2.circle(image, (cx, cy), 10, (0, 255, 0), 2)

                    return True, cx

        return False, 0

    def track_target(self, target_x, image_width):
        # Calculate error from center
        image_center = image_width / 2
        error = target_x - image_center

        # Proportional control
        angular_velocity = -self.kp * error

        # Create and publish command
        twist = Twist()
        twist.linear.x = min(self.max_speed, 0.3)
        twist.angular.z = angular_velocity

        self.cmd_vel_pub.publish(twist)

        self.get_logger().info(f'Tracking: error={error:.0f}')

    def search_for_target(self):
        # Rotate to search
        twist = Twist()
        twist.angular.z = 0.3

        self.cmd_vel_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectTrackingRobot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

---

##  Key Takeaways

 Integrate AI/ML models seamlessly with ROS 2
 Use parameters for dynamic configuration
 Launch files orchestrate multi-node systems
 URDF describes robot physical structure
 Combine vision, control, and decision-making

---

##  Next Module

**[Module 2: The Digital Twin →](../module-02-simulation/chapter-04-gazebo-physics)**

Learn physics simulation with Gazebo and photorealistic rendering with Unity!

---

** Questions?** Ask the chatbot about any code examples!
