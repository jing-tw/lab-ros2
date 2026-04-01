# Create a customized image that includes 
    1. humble-desktop-full   
    2. moveit2_tutorials
    3. ros-humble-ur-robot-driver

## Quick
```
# on host machine
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

```

## Test (on host)
```
# open another terminal
docker exec -it ur_humble_container bash

cd /ros2_ws
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash   # 如果你有自己的 workspace


# 執行你的腳本
python3 src/move_panda_moveit2.py
```

## clean (on host)
```
./clean.sh
```

## Build & Start
```
# on host machine
xhost +local:docker   # enable X11 
docker compose up -d --build  # start the container  (build: force to use customized Dockerfile)

```

## Into the container
```
docker exec -it ur_humble_container bash

```

## Pull dep & build
```
./01_init.sh
```

## Show the robot
```
# Show UR robot
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e  launch_rviz:=true

# Show Panda robot
ros2 launch moveit2_tutorials demo.launch.py rviz_tutorial:=true
```

## Clean 
```
# stops and removes the container, network, and default network volume.
docker compose down  

# removes both locally built images and pulled base images
docker compose down --rmi all 

```

# Reference
https://docs.google.com/document/d/17W982jvqyqAQ-Qc_H7OXPXbHFJvw3S9N9zEyenE1SG8/edit?usp=sharing

