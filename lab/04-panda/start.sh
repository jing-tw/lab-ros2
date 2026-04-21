#!/bin/bash
docker compose up -d # --build
xhost +local:docker
docker exec -it ur_humble_container bash


