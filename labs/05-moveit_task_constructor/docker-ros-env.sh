#!/bin/bash
# Usage:
#    source ./docker-ros-env.sh
# Important: You must use source (or .) when running the script, not ./docker-ros-env.sh

# Source ROS 2 Humble environment
source /opt/ros/humble/setup.bash

# Source your workspace's overlay (this must come AFTER the ROS base setup)
source /ros2_ws/install/setup.bash

echo "✅ ROS 2 Humble + workspace environment loaded successfully!"
echo "   ROS_DISTRO = $ROS_DISTRO"
echo "   Workspace  = /ros2_ws"