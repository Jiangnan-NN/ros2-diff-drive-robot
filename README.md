# ROS2 Differential Drive Robot

## Project Overview
This project focuses on developing a differential-drive mobile robot
using ROS2 Humble, starting from simulation and gradually moving toward
real hardware implementation.

## Development Environment
- Ubuntu 22.04
- ROS2 Humble
- Gazebo
- RViz2
- WSL2
- Git / GitHub

## Progress

### Week 1 – ROS2 Setup
- Installed Ubuntu 22.04 and ROS2 Humble
- Created ROS2 workspace
- Tested ROS2 publisher/subscriber communication
- Built the workspace using colcon
- Set up GitHub repository

### Week 2 – Robot Simulation
- Created differential-drive robot model
- Launched the robot in Gazebo
- Added differential-drive control
- Tested robot movement using teleoperation
- Visualized the robot in RViz

### Week 3 – LiDAR and Mapping
- Integrated LiDAR sensor into the robot model
- Verified `/scan` topic
- Visualized LiDAR data in RViz
- Integrated SLAM
- Successfully generated a map while driving the robot in Gazebo

## Current Status
The robot can currently:
- Spawn in Gazebo
- Move using keyboard teleoperation
- Publish LiDAR scan data
- Visualize sensor data in RViz
- Generate a map using SLAM

## Next Steps
- Improve simulation and sensor configuration
- Continue navigation development
- Prepare for integration with real hardware
