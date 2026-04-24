#!/bin/bash
docker compose up -d #--build
xhost +local:docker
docker exec -it ros2-container bash
# docker run -it --rm \
#   --name pinocchio-ros2 \
#   --network host \
#   --ipc host \
#   --privileged \
#   -e DISPLAY=$DISPLAY \
#   -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
#   0602-pinocchio-ros2-ros2-humble-service:latest


