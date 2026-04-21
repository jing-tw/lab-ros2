# Move Robot

## Quick
### MySRC example
```
# pull the source
git clone git@github.com:jing-tw/lab-ros2.git
goto the demo folder

# build image
. ./init_container.sh

# into the container
. ./start.sh

# dev
see src/mysrc/panda_ik/README.md

# clean
./clean._container.sh
```


## DEV 
```
# check the node, link, end_effector_name
ros2 run xacro xacro $(ros2 pkg prefix --share franka_description)/robots/fr3/fr3.urdf.xacro > /tmp/fr3.urdf
grep "joint name=" /tmp/fr3.urdf | head -10   # joint name
grep -E 'link name="fr3_link0"' /tmp/fr3.urdf # base link name
grep -E 'name="fr3_link[6-9]|fr3_hand|hand|flange|tcp' /tmp/fr3.urdf   # end effector name
```

# References
1. https://docs.google.com/document/d/17W982jvqyqAQ-Qc_H7OXPXbHFJvw3S9N9zEyenE1SG8/edit?usp=sharing
2. [ik, pinocchio] How to use Pinocchio in IK for Panda Robot, https://docs.google.com/document/d/1hA4pq42xYktnqphEHdOqoVa3RFcLyiuJ1hlpi4EwF_s/edit?usp=sharing

------
# ROS2 Quick
### Env Setup: create base docker image and show robots
```
# pull the source
git clone git@github.com:jing-tw/lab-ros2.git
goto the demo folder

# [host] create the base container
. ./init_container.sh

# [in container] install packages
. ./docker-entrypoint.sh

# [in container] show Panda robot
. ./install/setup.bash
ros2 launch moveit2_tutorials demo.launch.py rviz_tutorial:=true

# [in container] show UR robot
. /ros2_ws/install/setup.bash
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e  launch_rviz:=true

# [in container] show franka fr3 robot
ros2 launch franka_fr3_moveit_config moveit.launch.py robot_ip:=fake use_fake_hardware:=true
```

### Dev process
```
# [host] Get into the container
./start.sh

# [in container] move arm python script demo
cd /ros2_ws
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash  
python3 src/move_panda_moveit2.py    # move panda robot
python3 src/move_fr3_arm.py          # move fr3 robot

# [host] clean
./clean._container.sh
```


## DEV 
```
# check the node, link, end_effector_name
ros2 run xacro xacro $(ros2 pkg prefix --share franka_description)/robots/fr3/fr3.urdf.xacro > /tmp/fr3.urdf
grep "joint name=" /tmp/fr3.urdf | head -10   # joint name
grep -E 'link name="fr3_link0"' /tmp/fr3.urdf # base link name
grep -E 'name="fr3_link[6-9]|fr3_hand|hand|flange|tcp' /tmp/fr3.urdf   # end effector name
```