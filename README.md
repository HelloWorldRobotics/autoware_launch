# Autoware Buggy Configuration Guide

## Table of Contents
1. [Installation Guide](#installation-guide)
   - [Repository Setup](#repository-setup)
   - [Development Environment](#development-environment)
   - [Dependencies](#dependencies)
   - [Build Process](#build-process)
   - [Buggy Workspace](#buggy-workspace)
2. [Map Setup](#map-setup)
   - [MRANTI Map](#mranti-map)
   - [Foxglove Layouts](#foxglove-layouts)
3. [Hardware Setup](#hardware-setup)
   - [USB Device Configuration](#usb-device-configuration)
   - [LiDAR Configuration](#lidar-configuration)
4. [System Operation](#system-operation)
   - [Planning Simulator](#planning-simulator)
   - [Full System Launch](#full-system-launch)
5. [Configuration Changes](#configuration-changes)
   - [Behavioral Modifications](#behavioral-modifications)
   - [Parameter Tuning](#parameter-tuning)

## Installation Guide

### Repository Setup

Clone the September release repository:
```bash
git clone -b release/2024.09 https://github.com/HelloWorldRobotics/autoware.buggy.git
```

### Development Environment

Navigate to the repository and run the setup script:
```bash
cd ~/autoware.buggy
./setup-dev-env.sh
```

If you encounter NVIDIA/CUDA issues, run these commands and try the setup again:
```bash
sudo apt purge        \
  "cuda*"             \
  "libcudnn*"         \
  "libnvinfer*"       \
  "libnvonnxparsers*" \
  "libnvparsers*"     \
  "tensorrt*"         \
  "nvidia*"

sudo apt autoremove
```

### Dependencies

1. Import repositories:
```bash
mkdir src
vcs import src < autoware.repos
```

2. Add colcon ignore files for packages with modified versions in buggy_ws:
```bash
touch ~/autoware.buggy/src/universe/autoware.universe/common/tier4_state_rviz_plugin/COLCON_IGNORE
```

3. Setup ROS2 dependencies:
```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc && source ~/.bashrc
sudo apt update && sudo apt upgrade
rosdep update
rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
```

### Build Process

For a lighter but slower build, use:
```bash
MAKEFLAGS="-j1" colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release --executor sequential --packages-skip-build-finished --continue-on-error
```

> **Note**: You can adjust the build parameters:
> - `MAKEFLAGS="-j1"`: Change the number for parallel processes
> - `--executor sequential`: Change to `--parallel-workers <num>` for faster builds
> - If experiencing crashes, consider reducing parallel processes

### Buggy Workspace Setup

1. Clone the buggy workspace repository:
```bash
cd
git clone -b base_driver_split_test https://github.com/HelloWorldRobotics/buggy_ws.git
```

2. Import dependencies and build:
```bash
cd buggy_ws
vcs import src < buggy.repos
rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
colcon build --symlink-install
```

3. Setup CycloneDDS:
```bash
cd ~/buggy_ws/scripts
sudo chmod +x setup-cyclone.sh
./setup-cyclone.sh
```

4. Remove interfering programs:
```bash
sudo apt purge brltty -y
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager
```

## Map Setup

### MRANTI Map

1. Create and navigate to map directory:
```bash
mkdir ~/autoware_map
cd ~/autoware_map
```

2. Clone map repository and download pointcloud:
```bash
git clone -b big_map https://github.com/HelloWorldRobotics/mranti_lanelet
cd mranti_lanelet
wget -O pointcloud_map.pcd https://mclpfg.by.files.1drv.com/y4mIgi-DRT6UWYWphVCZ86OnfBGGD_ZsJ2tf6P_eqOflCyf20O61QQ_7nLyxCYw3RJnXHqQo0LNlCSLiCg6lgJAk0WlQPDdvb449qc0pQjA_1aF-BriFtpEGqeFJ1cZ-fFd3n-Txhk4uyd4zUtPLDxxsziqpJXkGCdkxdBKJ9C3b7kTLaXcIZDporF7Tsu1EmKOhG1n0p_HuSkbaUC4YPT7h3giNCGcF3Lkr7-OZqOLBgA?AVOverride=1
```

### Foxglove Layouts

Clone the layouts repository:
```bash
cd ~
git clone https://github.com/HelloWorldRobotics/foxglove_layouts.git
```

## Hardware Setup

### USB Device Configuration

1. Monitor USB devices by running these commands in separate terminals:
```bash
watch -n 0.3 'ls -l /dev/ttyUSB*'
watch -n 0.3 'ls -l /dev/ttyACM*'
```

2. Connect devices one at a time in this order:
   - PLC
   - Encoder
   - Steering
   - IMU

3. For each connected device, check its attributes:
```bash
udevadm -a -n /dev/ttyACM1 | grep -Ei "devpath|kernel|idvendor|idproduct|serial"
```

4. Create udev rules:
```bash
sudo nano /etc/udev/rules.d/10-buggy.rules
```

Example rules:
```
KERNEL=="ttyUSB*", ATTRS{idProduct}=="ea60", ATTRS{idVendor}=="10c4", MODE="0777", ATTRS{serial}=="0001", SYMLINK+="buggy_imu"
KERNEL=="ttyUSB*", ATTRS{idProduct}=="6001", ATTRS{idVendor}=="0403", MODE="0777", ATTRS{serial}=="B001AYFZ", SYMLINK+="buggy_base_wheel"
KERNEL=="ttyUSB*", ATTRS{idProduct}=="6001", ATTRS{idVendor}=="0403", MODE="0777", ATTRS{serial}=="B001BB26", SYMLINK+="buggy_base_encoder"
KERNEL=="ttyACM*", KERNELS=="1-7.4.1:1.6", MODE="0777", SYMLINK+="buggy_base_steering"
```

> **Important**: Avoid using devpath or USB port paths when possible, as this binds the rule to specific USB ports. The device should be recognized on any port connected, though this may not be possible for all devices.

5. Apply and reload udev rules:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

6. Verify rules are applied:
```bash
ls -l /dev/bugg*
```
This should show all four devices defined in the rules.

### LiDAR Configuration

1. Monitor network interfaces:
```bash
watch -n 0.3 'ip a'
```

2. Connect LiDARs one by one, noting the MAC address of each ethernet port (e.g., link/ether 6c:a1:00:06:25:9a)

3. Add LiDAR udev rules to the existing rules file:
```bash
sudo nano /etc/udev/rules.d/10-buggy.rules
```

Example LiDAR rules:
```
SUBSYSTEM=="net", ACTION=="add", ATTRS{address}=="78:d0:04:33:ec:38", KERNEL=="enp0s31f6", NAME="lidar_top"
SUBSYSTEM=="net", ACTION=="add", ATTRS{address}=="78:d0:04:34:45:c1", KERNEL=="enp2s0", NAME="lidar_right"
SUBSYSTEM=="net", ACTION=="add", ATTRS{address}=="78:d0:04:34:45:c2", KERNEL=="enp3s0", NAME="lidar_left"
```

4. Configure netplan:
```bash
sudo nano /etc/netplan/01-network-manager-all.yaml
sudo netplan apply
```

5. Test LiDAR communication:
```bash
sudo tcpdump -n -i lidar_top
```

6. Test LiDAR drivers:
```bash
source ~/autoware.buggy/install/setup.bash
source ~/buggy_ws/install/setup.bash
ros2 launch autoware_launch lidars_only.launch.xml
```

7. In a new terminal, launch Foxglove bridge:
```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml
```

Then visualize the pointcloud topics in Foxglove to verify.

## System Operation

### Source Workspaces
```bash
source ~/autoware.buggy/install/setup.bash
source ~/buggy_ws/install/setup.bash
```

### Planning Simulator
Launch the planning simulator:
```bash
ros2 launch autoware_launch planning_simulator.launch.xml map_path:=[YOUR_MAP_FOLDER_HERE] vehicle_model:=buggy_vehicle sensor_model:=buggy_sensor_kit
```

### Full System Launch

1. Launch Autoware nodes (Terminal 1):
```bash
source ~/autoware.buggy/install/setup.bash
source ~/buggy_ws/install/setup.bash
ros2 launch autoware_launch autoware.launch.xml map_path:=$HOME/autoware_map/mranti_lanelet
```

2. Launch drivers and utilities (Terminal 2):
```bash
source ~/autoware.buggy/install/setup.bash
source ~/buggy_ws/install/setup.bash
ros2 launch buggy_bringup buggy_bringup.launch.xml buggy_no:=1
```

> **Tip**: To make launching faster, explore the scripts in `~/buggy_ws/scripts` and consider adding them to your bash aliases.

## Configuration Changes

### Behavioral Modifications
- Vehicle-specific parameters and sensor transformations are stored in `autoware_individual_params`
- Sensor transformations include:
  - Multiple cameras (camera0, camera1, camera2, traffic light cameras)
  - LiDAR sensors (velodyne_top, velodyne_left, velodyne_right)
  - GNSS
  - IMU

### Parameter Tuning
Parameters that were changed are stated in the following README.md file: [Parameter Tuning README](parameter_change.md)

> **Note**: Always test parameter changes in simulation before deploying to the real vehicle.





