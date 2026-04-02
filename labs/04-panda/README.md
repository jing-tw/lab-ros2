# Move Robot

## Quick
```
# pull the source
git clone git@github.com:jing-tw/lab-ros2.git
cd labs/03-moveit-move-arm

# start the container
# docker exec -it ur_humble_container bash
. ./init.sh

# prepare the packages (in container)
. ./docker-entrypoint.sh

# show Panda robot
. /ros2_ws/install/setup.bash
ros2 launch moveit2_tutorials demo.launch.py rviz_tutorial:=true

# show UR robot
. /ros2_ws/install/setup.bash
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e  launch_rviz:=true

# show franka fr3 robot
ros2 launch franka_fr3_moveit_config moveit.launch.py robot_ip:=fake use_fake_hardware:=true

# into the container
./start.sh

# run script
cd /ros2_ws
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash  
python3 src/move_panda_moveit2.py

# clean
./clean.sh
```


## DEV 
```
# check the node, link, end_effector_name
ros2 run xacro xacro $(ros2 pkg prefix --share franka_description)/robots/fr3/fr3.urdf.xacro > /tmp/fr3.urdf
grep "joint name=" /tmp/fr3.urdf | head -10   # joint name
grep -E 'link name="fr3_link0"' /tmp/fr3.urdf # base link name
grep -E 'name="fr3_link[6-9]|fr3_hand|hand|flange|tcp' /tmp/fr3.urdf   # end effector name
```

# Reference
https://docs.google.com/document/d/17W982jvqyqAQ-Qc_H7OXPXbHFJvw3S9N9zEyenE1SG8/edit?usp=sharing

