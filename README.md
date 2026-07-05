<div align="center">

# 🤖 Warehouse AMR Simulation

### Autonomous Mobile Robot Simulation using NVIDIA Isaac Sim, ROS 2 Jazzy & SLAM Toolbox

[![ROS 2](https://img.shields.io/badge/ROS%202-Jazzy-blue?style=for-the-badge&logo=ros)](https://docs.ros.org/en/jazzy/)
[![Isaac Sim](https://img.shields.io/badge/NVIDIA-Isaac%20Sim-76b900?style=for-the-badge&logo=nvidia)](https://developer.nvidia.com/isaac-sim)
[![SLAM](https://img.shields.io/badge/SLAM-Toolbox-orange?style=for-the-badge)](https://github.com/SteveMacenski/slam_toolbox)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?style=for-the-badge&logo=ubuntu)](https://ubuntu.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)

<br/>

**Author:** Anirudhha Veeranagaiah M

<br/>

[![Demo Video](https://img.shields.io/badge/▶%20Watch%20Demo-Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1-T69V76DVFmAXzxdJ3wBmEMlk4N4TLv6/view?usp=sharing)

</div>

---

## 📖 Overview

This project delivers a **complete simulation pipeline** for a Warehouse Autonomous Mobile Robot (AMR) built from scratch using **NVIDIA Isaac Sim** and **ROS 2 Jazzy**. The robot is a custom-assembled differential-drive platform capable of:

- 📡 Publishing real-time **LiDAR** and **Odometry** data to ROS 2
- 🗺️ Generating live **2D occupancy maps** via SLAM Toolbox
- 🔁 Maintaining a correct **TF transform tree** for sensor fusion
- 👁️ Visualizing everything in **RViz2**

Rather than relying on a pre-built pipeline, the entire stack — from robot assembly to SLAM integration — was built and debugged manually, providing deep practical experience in ROS 2 middleware, coordinate frames, and simulation physics.

---

## 🎯 Objectives

- ✅ Build a **custom warehouse robot** inside Isaac Sim
- ✅ Integrate Isaac Sim with **ROS 2 Jazzy** via the ROS bridge
- ✅ Publish **LiDAR** (`/scan`) and **Odometry** (`/odom`) data
- ✅ Construct a correct **TF tree**: `map → odom → base_link → sim_lidar`
- ✅ Perform real-time **2D SLAM** using SLAM Toolbox
- ✅ Visualize the occupancy map in **RViz2**
- ✅ Understand end-to-end **ROS 2 communication**

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| **Ubuntu** | 24.04 LTS | Operating System |
| **ROS 2** | Jazzy | Robotics Middleware |
| **NVIDIA Isaac Sim** | Latest | Physics-based Robot Simulation |
| **SLAM Toolbox** | Latest | 2D LiDAR SLAM |
| **RViz2** | — | Visualization |
| **Python** | 3.12 | Custom Node Development |

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       NVIDIA Isaac Sim                           │
│                                                                  │
│   Differential-Drive Robot  →  ROS Bridge  →  /scan             │
│                                            →  /odom             │
│                                            →  /cmd_vel          │
│                                            →  /clock            │
└──────────────────────────┬───────────────────────────────────────┘
                           │ ROS 2 DDS
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                     Custom ROS 2 Nodes                           │
│                                                                  │
│   odom_filter_2d     ─── Filters 3D odom → 2D /odom_filtered    │
│   odom_tf_broadcaster ── Broadcasts odom → base_link TF         │
│   static_lidar_tf    ─── Publishes base_link → sim_lidar TF     │
└──────────────────────────┬───────────────────────────────────────┘
                           │ TF Tree + LaserScan
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      SLAM Toolbox                                │
│                                                                  │
│   map → odom → base_link → sim_lidar                            │
│                  ↓                                               │
│           Occupancy Grid Map  →  RViz2                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📦 Package Structure

```
warehouse_amr_ws/
├── src/
│   └── warehouse_amr/
│       ├── warehouse_amr/
│       │   ├── odom_filter_2d.py        # 3D → 2D odometry filter
│       │   ├── odom_tf_broadcaster.py   # odom → base_link TF broadcaster
│       │   └── static_lidar_tf.py       # base_link → sim_lidar static TF
│       ├── setup.py
│       └── package.xml
├── config/
│   └── slam_params.yaml                 # SLAM Toolbox configuration
└── Media/                               # Screenshots & demo assets
```

---

## ⚙️ Custom ROS 2 Nodes

### 1. `odom_filter_2d` — Odometry Filter
Isaac Sim's physics engine introduces minor **3D noise** (Z-axis drift, roll, pitch) even for a ground-based robot. This node:
- Subscribes to `/odom`
- Strips Z-position, roll, and pitch
- Retains only **X, Y, and Yaw**
- Publishes clean `/odom_filtered` for SLAM consumption

### 2. `odom_tf_broadcaster` — TF Broadcaster
SLAM Toolbox requires a live `odom → base_link` TF transform. This node:
- Subscribes to `/odom_filtered`
- Broadcasts the **`odom → base_link`** transform
- Uses the **odometry message timestamp** (not system clock) to prevent sync issues

### 3. `static_lidar_tf` — Static LiDAR Transform
Since the LiDAR is rigidly mounted, its transform is invariant. This node:
- Continuously publishes the **`base_link → sim_lidar`** static transform
- Ensures scan data is correctly registered in the robot's coordinate frame

---

## 🌳 TF Tree

```
map
 └── odom                    ← Published by SLAM Toolbox
      └── base_link          ← Published by odom_tf_broadcaster
           └── sim_lidar     ← Published by static_lidar_tf
```

---

## 🚀 Getting Started

### Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy ([Installation Guide](https://docs.ros.org/en/jazzy/Installation.html))
- NVIDIA Isaac Sim ([Download](https://developer.nvidia.com/isaac-sim))
- SLAM Toolbox

```bash
sudo apt install ros-jazzy-slam-toolbox
```

### Build

```bash
# Clone the repository
git clone <your-repo-url>
cd warehouse_amr_ws

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
colcon build

# Source the workspace
source install/setup.bash
```

### Run

**Terminal 1 — Launch NVIDIA Isaac Sim** with the warehouse scene and enable the ROS bridge.

**Terminal 2 — Start the custom ROS 2 nodes:**

```bash
source install/setup.bash

# Start odometry filter
ros2 run warehouse_amr odom_filter_2d

# Start TF broadcaster
ros2 run warehouse_amr odom_tf_broadcaster

# Start static LiDAR transform
ros2 run warehouse_amr static_lidar_tf
```

**Terminal 3 — Launch SLAM Toolbox:**

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=config/slam_params.yaml \
  use_sim_time:=true
```

**Terminal 4 — Visualize in RViz2:**

```bash
rviz2
```
> Add the `/map` topic and set the fixed frame to `map`.

**Terminal 5 — Teleoperate the robot:**

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 🔧 SLAM Configuration Highlights

Key parameters in `config/slam_params.yaml`:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `base_frame` | `base_link` | Robot base frame |
| `scan_topic` | `/scan` | LiDAR input topic |
| `odom_frame` | `odom` | Odometry frame |
| `map_frame` | `map` | Global map frame |
| `resolution` | `0.05` | Map resolution (5 cm/cell) |
| `mode` | `mapping` | Active SLAM mode |
| `max_laser_range` | `20.0` m | Maximum LiDAR range |

---

## 🐛 Challenges & Debugging

| Challenge | Root Cause | Resolution |
|-----------|-----------|------------|
| SLAM Toolbox failure at start | Missing TF tree | Built complete `odom → base_link → sim_lidar` chain |
| Nodes not found after build | Incorrect `setup.py` console scripts | Fixed entry point configuration |
| TF timestamp mismatch | Used system clock instead of sim clock | Switched to odometry message timestamp |
| LiDAR scans not registering | Frame name mismatch (`lidar` vs `sim_lidar`) | Unified frame IDs across all nodes |
| SLAM expected `base_footprint` | Default SLAM Toolbox config | Created custom `slam_params.yaml` with `base_link` |
| Zero simulation clock | Isaac Sim not running when bridge launched | Ensured sim is playing before launching ROS nodes |
| Odometry noise | Physics engine introduces 3D motion | Built `odom_filter_2d` node to project to 2D |
| Invalid LiDAR transform | Rigid body on sensor mount allowed movement | Removed rigid body component from mount |

---

## 📊 Results

- ✅ **Full ROS 2 ↔ Isaac Sim integration** established
- ✅ **LaserScan** and **Odometry** published correctly
- ✅ **TF tree** (`map → odom → base_link → sim_lidar`) fully operational
- ✅ **Simulation clock** synchronized across all nodes
- ✅ **Real-time occupancy map** generated and visualized in RViz2
- ✅ Robot successfully **teleoperated** while SLAM runs

---

## 🔮 Future Work

- [ ] Upgrade to a production-grade mobile robot model
- [ ] Integrate **Navigation2 (Nav2)** for autonomous navigation
- [ ] Implement **waypoint following** and **obstacle avoidance**
- [ ] **Localization on saved maps** using AMCL
- [ ] Add **camera-based perception** and object detection
- [ ] **Multi-robot coordination** for warehouse fleet management

---

## 📚 Lessons Learned

This project provided hands-on experience with:

- ROS 2 publishers, subscribers, and service interfaces
- TF2 transform trees and coordinate frame management
- LiDAR sensor integration and scan processing
- Simulation clock synchronization (`use_sim_time`)
- Odometry processing and noise filtering
- SLAM Toolbox configuration and tuning
- Debugging robotics middleware integration

---

## 📄 License

This project is for educational and research purposes.

---

<div align="center">

**Built with ❤️ using NVIDIA Isaac Sim + ROS 2 Jazzy**

[![Demo Video](https://img.shields.io/badge/▶%20Watch%20Full%20Demo-Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1-T69V76DVFmAXzxdJ3wBmEMlk4N4TLv6/view?usp=sharing)

</div>
