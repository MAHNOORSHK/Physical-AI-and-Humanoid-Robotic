---
sidebar_position: 20
title: Hardware Requirements
---

# Hardware Requirements

##  System Requirements

This course is technically demanding, sitting at the intersection of:
- **Physics Simulation** (Isaac Sim/Gazebo)
- **Visual Perception** (SLAM/Computer Vision)
- **Generative AI** (LLMs/VLA)

---

##  Required Hardware

### 1. Development Workstation (Required)

This is the most critical component. NVIDIA Isaac Sim requires **RTX** capabilities.

**Minimum Specifications:**
- **GPU:** NVIDIA RTX 3060 (12GB VRAM)
- **CPU:** Intel Core i5 (12th Gen) or AMD Ryzen 5
- **RAM:** 32 GB DDR4
- **Storage:** 512 GB SSD
- **OS:** Ubuntu 22.04 LTS

**Recommended Specifications:**
- **GPU:** NVIDIA RTX 4070 Ti (12GB VRAM) or RTX 4090 (24GB VRAM)
- **CPU:** Intel Core i7 (13th Gen+) or AMD Ryzen 9
- **RAM:** 64 GB DDR5
- **Storage:** 1 TB NVMe SSD
- **OS:** Ubuntu 22.04 LTS (dual-boot or dedicated)

**Why RTX GPU?**
- High VRAM for Isaac Sim USD assets
- Ray tracing for photorealistic rendering
- CUDA acceleration for AI/ML models
- TensorRT for optimized inference

---

### 2. Edge AI Kit (Optional - For Physical Deployment)

For students wanting to deploy to real hardware:

**Components:**

| Component | Model | Price | Purpose |
|-----------|-------|-------|---------|
| **The Brain** | NVIDIA Jetson Orin Nano Super (8GB) | $249 | Edge AI computing (40 TOPS) |
| **The Eyes** | Intel RealSense D435i | $349 | RGB-D camera with IMU |
| **The Ears** | ReSpeaker USB Mic Array v2.0 | $69 | Far-field voice commands |
| **Storage** | 128GB microSD (High Endurance) | $30 | OS and data storage |
| **Total** | | **~$700** | Complete edge kit |

---

### 3. Cloud Alternative (Pay-as-you-go)

If you don't have a powerful workstation:

**AWS/Azure GPU Instance:**
- **Instance Type:** AWS g5.2xlarge (A10G GPU, 24GB VRAM)
- **Cost:** ~$1.50/hour
- **Usage:** 10 hours/week × 12 weeks = 120 hours
- **Total:** ~$180 for the course

**Pros:**
- No upfront hardware cost
- Access latest GPUs
- Scalable resources

**Cons:**
- Ongoing costs
- Internet dependency
- Latency for interactive work

---

##  Software Requirements

### Operating System

**Mandatory:** Ubuntu 22.04 LTS (Jammy Jellyfish)

**Why Ubuntu 22.04?**
- ROS 2 Humble native support
- NVIDIA driver compatibility
- Isaac Sim official support
- Large robotics community

**Installation Options:**
1. **Dual Boot** (Recommended) - Native performance
2. **WSL2** - Windows users (limited GPU support)
3. **Virtual Machine** - Not recommended (no GPU passthrough)

---

### Core Software Stack

#### 1. ROS 2 Humble
```bash
# Installation
sudo apt install ros-humble-desktop
```
**Disk Space:** ~3 GB

#### 2. NVIDIA Drivers & CUDA
```bash
# Install NVIDIA driver
sudo apt install nvidia-driver-535

# Install CUDA Toolkit
sudo apt install nvidia-cuda-toolkit
```
**Disk Space:** ~5 GB

#### 3. Isaac Sim (Optional for Advanced Modules)
**Disk Space:** ~50 GB
**Download:** [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)

#### 4. Development Tools
```bash
sudo apt install python3-pip
sudo apt install git
sudo apt install terminator  # Multiple terminals
pip3 install opencv-python numpy matplotlib
```

---

##  Hardware Options Comparison

### Option A: Budget Setup ($0 - Software Only)

**What you can do:**
-  Complete Module 1 (ROS 2)
-  Basic Gazebo simulation
-  Code all examples
-  Isaac Sim (requires RTX)
-  Real-time perception

**Hardware:**
- Any laptop with Ubuntu
- 8GB RAM minimum
- Integrated graphics OK

---

### Option B: Standard Setup ($1,500 - $2,500)

**What you can do:**
-  All course modules
-  Isaac Sim (medium quality)
-  Real-time perception
-  Train small ML models
-  Limited multi-tasking

**Hardware:**
- Desktop PC or laptop
- RTX 3060/3070 GPU
- 32GB RAM
- 512GB SSD

---

### Option C: Optimal Setup ($3,000 - $5,000)

**What you can do:**
-  Everything in Option B
-  Isaac Sim (high quality)
-  Train large models
-  Multiple VMs/containers
-  Future-proof for 5+ years

**Hardware:**
- Desktop workstation
- RTX 4080/4090 GPU
- 64GB+ RAM
- 1TB+ NVMe SSD

---

### Option D: Cloud-Based ($180 - $300)

**What you can do:**
-  All course modules
-  Isaac Sim on demand
-  No upfront investment
-  Internet dependency

**Cost:**
- AWS/Azure GPU instance
- $1.50/hour
- ~$200 for course

---

##  Recommendations by Student Type

### Hobbyist / Beginner
→ **Option A or B**
- Start with ROS 2 on any laptop
- Upgrade if continuing

### Professional / Career Change
→ **Option C**
- Investment pays off
- Use for future projects

### Cost-Conscious Student
→ **Option D (Cloud)**
- No upfront cost
- Pay as you learn

### Research / Industry
→ **Option C + Edge Kit**
- Complete development stack
- Deploy to real hardware

---

##  Performance Benchmarks

### Isaac Sim Frame Rates

| GPU | Resolution | FPS | Quality |
|-----|------------|-----|---------|
| RTX 3060 | 1080p | 15-20 | Medium |
| RTX 4070 Ti | 1080p | 40-60 | High |
| RTX 4090 | 4K | 60+ | Ultra |

### Gazebo Simulation

| Hardware | Complex Scene FPS |
|----------|-------------------|
| Integrated GPU | 5-10 |
| GTX 1660 | 20-30 |
| RTX 3060+ | 60+ |

---

##  Setup Verification

After installation, verify your setup:

```bash
# Check ROS 2
ros2 --version

# Check GPU
nvidia-smi

# Check CUDA
nvcc --version

# Check Python packages
python3 -c "import cv2; print(cv2.__version__)"
python3 -c "import torch; print(torch.__version__)"
```

---

##  Tips for Success

1. **Start Simple** - Don't wait for perfect hardware
2. **Ubuntu Native** - Virtual machines cause issues
3. **SSD is Critical** - Isaac Sim needs fast storage
4. **RAM Matters** - 32GB minimum for serious work
5. **Cloud for Peaks** - Use cloud for heavy simulations

---

##  Common Questions

**Q: Can I use macOS or Windows?**
A: Some modules work, but Ubuntu 22.04 is strongly recommended.

**Q: Is RTX GPU mandatory?**
A: No for Modules 1-2. Yes for Module 3 (Isaac Sim).

**Q: Can I use Jetson for development?**
A: Jetson is for deployment. Use x86 workstation for development.

**Q: What about AMD GPUs?**
A: Not supported for CUDA/Isaac Sim. NVIDIA only.

---

##  Need Help?

Having hardware issues? Ask the chatbot or check:
- [ROS 2 System Requirements](https://docs.ros.org/en/humble/)
- [Isaac Sim Requirements](https://docs.omniverse.nvidia.com/isaacsim/)
- [NVIDIA Driver Installation](https://ubuntu.com/server/docs/nvidia-drivers-installation)

---

**Next:** [Lab Setup Guide →](./lab-setup)
