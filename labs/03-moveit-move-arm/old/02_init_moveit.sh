#!/bin/bash
cd /ros2_ws/src
git clone https://github.com/moveit/moveit2.git -b humble   # pull moveit2 source

cd /ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select moveit_core moveit_ros_planning moveit_py
source /ros2_ws/install/setup.bash

# verification
ros2 pkg list | grep moveit_core
ros2 pkg list | grep moveit_ros_planning
ros2 pkg list | grep moveit_py

# run the python test
python3 -c "from moveit.planning import MoveItPy; print('成功！')"