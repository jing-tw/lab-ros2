#!/bin/bash
mkdir -p src
cd /ros2_ws/src
git clone -b humble https://github.com/ros-planning/moveit2_tutorials.git

cd /ros2_ws
rm -rf build/ install/ log/

cd /ros2_ws
rosdep update
apt-get update
rosdep install -r --from-paths src --ignore-src --rosdistro humble -y

colcon build --symlink-install --packages-select moveit2_tutorials
source /ros2_ws/install/setup.bash

# verification
ros2 pkg list | grep moveit2_tutorials