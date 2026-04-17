# Create a customized image that includes 
    1. humble-desktop-full   
    2. moveit2_tutorials
    3. ros-humble-ur-robot-driver
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

## Run the script
```
./01_clone_moveit_tutorials.sh
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
