#!/bin/bash
docker compose up -d
xhost +local:docker
docker exec -it ur_humble_container bash


