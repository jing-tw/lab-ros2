#!/bin/bash
set -e  # Exit on any error
#!/bin/bash
# mkdir -p src
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


# ======= moveit2 =======
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

# ====== pymoveit2 =====
cd /ros2_ws/src

# clone
# install & build (official, full package, https://github.com/AndrejOrsula/pymoveit2)
# git clone https://github.com/AndrejOrsula/pymoveit2.git
# cd /ros2_ws
# rosdep install -y -r -i --rosdistro ${ROS_DISTRO} --from-paths .
# colcon build --symlink-install --cmake-args "-DCMAKE_BUILD_TYPE=Release"
# source install/setup.bash

# Old (pymoveit2 minimal, only the python wrapper
git clone https://github.com/AndrejOrsula/pymoveit2.git
cd /ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select pymoveit2 --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash

# verify
python3 -c "from pymoveit2 import MoveIt2; print('✅ pymoveit2 安裝成功！')"

echo 'source /ros2_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc


