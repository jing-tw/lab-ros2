#!/bin/bash
# xhost +local:docker
# docker compose up -d --build 
# docker exec -it ur_humble_container bash

# echo "If you got the container running message, docker rm -f ur_humble_container"

#!/bin/bash

# --- Configuration ---
CONTAINER_NAME="ur_humble_container"
COMPOSE_FILE="docker-compose.yml" # Assuming your compose file is named this

# --- Functions ---

# Function to check if a container exists and is running
check_container_status() {
  docker ps -f name="${CONTAINER_NAME}" --format "{{.Status}}" | grep -q "Up"
}

# --- Main Script ---

echo "--- Preparing Docker environment ---"

# Allow Docker containers to access the host's X server for GUI applications
echo "Granting local X server access to Docker..."
xhost +local:docker || { echo "ERROR: Failed to grant X server access. Do you have xhost installed?"; exit 1; }

echo "--- Starting/Building Docker Compose services ---"

# Build and start services defined in the docker-compose.yml file in detached mode
# The --build flag ensures images are rebuilt if necessary
docker compose -f "${COMPOSE_FILE}" up -d --build || { echo "ERROR: Docker Compose failed to start services. See above for details."; exit 1; }

echo "--- Connecting to the container ---"

# Check if the container is running before attempting to exec into it
if check_container_status; then
  echo "Container '${CONTAINER_NAME}' is running. Attaching interactive bash session..."
  docker exec -it "${CONTAINER_NAME}" bash
else
  echo "WARNING: Container '${CONTAINER_NAME}' is not running. Cannot attach interactive session."
  echo "Please check 'docker ps -a' for container status."
fi

echo "--- Script Finished ---"
echo "If you encountered issues or wish to restart, remember to stop and remove the container first:"
echo "docker rm -f ${CONTAINER_NAME}"
echo "docker compose -f ${COMPOSE_FILE} down"

echo "Next: source ./docker-entrypoint.sh"