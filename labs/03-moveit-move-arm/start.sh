#!/bin/bash
xhost +local:docker
docker compose up -d --build 
docker exec -it ur_humble_container bash
