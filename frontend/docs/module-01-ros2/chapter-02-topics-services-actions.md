---
sidebar_position: 2
title: Chapter 2 - Topics, Services & Actions
---

# Chapter 2: Topics, Services, and Actions

**⏱ Week 3-4, Days 3-7** | ** Module 1: The Robotic Nervous System**

---

##  Learning Objectives

By the end of this chapter, you will:

-  Implement publisher-subscriber communication with topics
-  Create synchronous request-response patterns with services
-  Build long-running tasks with feedback using actions
-  Choose appropriate communication patterns for robotics tasks
-  Understand Quality of Service (QoS) policies

---

##  Part 1: Topics (Publish-Subscribe)

### What are Topics?

**Topics** enable **asynchronous, many-to-many** communication between nodes.

**Key Characteristics:**
- **Fire and forget** - Publishers don't wait for subscribers
- **Streaming data** - Continuous sensor data
- **Decoupled** - Publishers and subscribers don't know about each other
- **Many-to-many** - Multiple publishers and subscribers on same topic

### When to Use Topics

 Streaming sensor data (camera, LiDAR, IMU)
 Robot state updates (position, velocity)
 Continuous monitoring (battery level)
 Broadcasting information to multiple nodes

---

### Creating a Publisher

Let's create a battery monitor that publishes battery percentage.

**File:** `battery_publisher.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryPublisher(Node):
    def __init__(self):
        super().__init__('battery_publisher')

        # Create publisher on /battery_level topic
        self.publisher = self.create_publisher(
            Float32,           # Message type
            'battery_level',   # Topic name
            10                 # Queue size
        )

        # Publish every 1 second
        self.timer = self.create_timer(1.0, self.publish_battery)
        self.battery_level = 100.0

        self.get_logger().info('Battery publisher started')

    def publish_battery(self):
        msg = Float32()
        msg.data = self.battery_level

        self.publisher.publish(msg)
        self.get_logger().info(f'Published: {self.battery_level}%')

        # Simulate battery drain
        self.battery_level -= 0.5
        if self.battery_level < 0:
            self.battery_level = 100.0

def main(args=None):
    rclpy.init(args=args)
    node = BatteryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### Creating a Subscriber

Now let's create a node that monitors battery level and warns when low.

**File:** `battery_subscriber.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatterySubscriber(Node):
    def __init__(self):
        super().__init__('battery_subscriber')

        # Create subscriber
        self.subscription = self.create_subscription(
            Float32,
            'battery_level',
            self.battery_callback,
            10
        )

        self.get_logger().info('Battery monitor started')

    def battery_callback(self, msg):
        battery = msg.data

        if battery < 20.0:
            self.get_logger().warn(f' LOW BATTERY: {battery:.1f}%')
        elif battery < 50.0:
            self.get_logger().info(f'Battery: {battery:.1f}%')
        else:
            self.get_logger().info(f' Battery OK: {battery:.1f}%')

def main(args=None):
    rclpy.init(args=args)
    node = BatterySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### Custom Messages

Let's create a custom message for robot pose.

**Step 1:** Create message file

**File:** `msg/RobotPose.msg`
```
float64 x
float64 y
float64 theta
float64 velocity
string status
```

**Step 2:** Update `package.xml`
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

**Step 3:** Update `CMakeLists.txt`
```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotPose.msg"
)
```

**Step 4:** Use custom message
```python
from my_package.msg import RobotPose

# Publishing
msg = RobotPose()
msg.x = 1.5
msg.y = 2.3
msg.theta = 0.785
msg.velocity = 0.5
msg.status = 'moving'
publisher.publish(msg)
```

---

### Quality of Service (QoS)

QoS policies control message delivery behavior.

**Common QoS Profiles:**

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# Sensor data (lossy, latest only)
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    depth=10
)

# Critical data (reliable, persistent)
reliable_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    depth=10
)

# Create publisher with custom QoS
self.publisher = self.create_publisher(
    Float32,
    'critical_data',
    reliable_qos
)
```

**When to use each:**
- **BEST_EFFORT:** High-frequency sensor data (camera, LiDAR)
- **RELIABLE:** Commands, state changes, critical data

---

##  Part 2: Services (Request-Response)

### What are Services?

**Services** provide **synchronous, one-to-one** communication.

**Key Characteristics:**
- **Request-response** - Client waits for server response
- **Synchronous** - Blocking call
- **One-to-one** - Single client talks to single server
- **Short operations** - Not for long-running tasks

### When to Use Services

 Configuration changes
 One-time queries (get robot state)
 Triggering specific actions
 System health checks

---

### Creating a Service Server

Let's create a service to reset the robot's odometry.

**File:** `reset_odom_server.py`

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetOdomServer(Node):
    def __init__(self):
        super().__init__('reset_odom_server')

        self.srv = self.create_service(
            Trigger,
            'reset_odometry',
            self.reset_callback
        )

        self.get_logger().info('Reset odometry service ready')

    def reset_callback(self, request, response):
        # Perform reset operation
        self.get_logger().info('Resetting odometry...')

        # Simulate reset logic
        # In real robot: reset_odometry_hardware()

        response.success = True
        response.message = 'Odometry reset successfully'

        return response

def main(args=None):
    rclpy.init(args=args)
    node = ResetOdomServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### Creating a Service Client

**File:** `reset_odom_client.py`

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetOdomClient(Node):
    def __init__(self):
        super().__init__('reset_odom_client')

        self.client = self.create_client(Trigger, 'reset_odometry')

        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send_request(self):
        request = Trigger.Request()

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            response = future.result()
            self.get_logger().info(
                f'Result: {response.success}, {response.message}'
            )
        else:
            self.get_logger().error('Service call failed')

def main(args=None):
    rclpy.init(args=args)
    node = ResetOdomClient()
    node.send_request()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### Custom Service

**File:** `srv/SetSpeed.srv`
```
float64 linear_speed
float64 angular_speed
---
bool success
string message
```

**Usage:**
```python
from my_package.srv import SetSpeed

def set_speed_callback(self, request, response):
    linear = request.linear_speed
    angular = request.angular_speed

    # Set robot speed
    self.get_logger().info(f'Setting speed: {linear}, {angular}')

    response.success = True
    response.message = f'Speed set to {linear}m/s'
    return response
```

---

##  Part 3: Actions (Goal-Feedback-Result)

### What are Actions?

**Actions** are for **long-running tasks** with **feedback**.

**Key Characteristics:**
- **Goal** - What to do
- **Feedback** - Progress updates
- **Result** - Final outcome
- **Preemptable** - Can be canceled

### When to Use Actions

 Navigation to a goal
 Manipulation tasks
 Long computations with progress
 Any task that takes >1 second

---

### Action Structure

```
Goal:
  target_x: 5.0
  target_y: 3.0
---
Result:
  final_x: 5.01
  final_y: 2.98
  success: true
---
Feedback:
  current_x: 2.5
  current_y: 1.8
  distance_remaining: 3.2
```

---

### Creating an Action Server

**File:** `navigate_action_server.py`

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci
import time

class NavigateActionServer(Node):
    def __init__(self):
        super().__init__('navigate_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,  # Using Fibonacci as example
            'navigate',
            self.execute_callback
        )

        self.get_logger().info('Navigate action server ready')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        # Get goal
        order = goal_handle.request.order

        # Feedback object
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        # Execute with feedback
        for i in range(1, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            # Simulate progress
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] +
                feedback_msg.partial_sequence[i-1]
            )

            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        # Return result
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    node = NavigateActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### Creating an Action Client

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci

class NavigateActionClient(Node):
    def __init__(self):
        super().__init__('navigate_action_client')
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'navigate'
        )

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Progress: {feedback.partial_sequence}')

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')

def main(args=None):
    rclpy.init(args=args)
    node = NavigateActionClient()
    node.send_goal(10)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

---

##  Communication Pattern Comparison

| Feature | Topics | Services | Actions |
|---------|--------|----------|---------|
| **Pattern** | Publish-Subscribe | Request-Response | Goal-Feedback-Result |
| **Timing** | Asynchronous | Synchronous | Asynchronous |
| **Cardinality** | Many-to-Many | One-to-One | One-to-One |
| **Duration** | Continuous | Instant | Long-running |
| **Feedback** | No | No | Yes |
| **Cancellable** | N/A | No | Yes |
| **Use Case** | Sensor data | Config changes | Navigation |

---

##  Hands-On Labs

### Lab 1: Robot Speed Controller

Create a system with:
1. **Publisher:** Publishes target speed
2. **Subscriber:** Receives speed and controls motors
3. **Service:** Emergency stop

### Lab 2: Battery Management System

Build a complete battery system:
- **Topic:** Battery percentage (publisher/subscriber)
- **Service:** Reset battery to 100%
- **Action:** Charging process with feedback

### Lab 3: Navigation System

Implement a basic navigation system:
- **Action Server:** Move to goal with feedback
- **Action Client:** Send navigation goals
- **Topic:** Publish current position

---

##  Key Takeaways

 Use **topics** for streaming data (sensor readings)
 Use **services** for quick request-response (config changes)
 Use **actions** for long tasks with feedback (navigation)
 QoS policies control reliability and durability
 Custom messages/services/actions for specific needs

---

##  Next Chapter

**[Chapter 3: Building Robot Systems with rclpy →](./chapter-03-building-with-rclpy)**

Learn advanced rclpy patterns, integrate AI models, create URDF descriptions, and build complete robot systems.

---

** Questions?** Select any code example and ask the chatbot for clarification!
