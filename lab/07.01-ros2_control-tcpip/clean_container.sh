#!/bin/bash
# Remove
# (1) Removes images used by the services in compose
docker compose down --rmi all 
# (2) Remove all unused images (dangling + unused)
# docker image prune -a -f
# (3) More aggressive cleanup
# Remove everything unused: stopped containers, unused images, networks, build cache
# docker system prune -a -f --volumes

# clean the previous build and install files
read -p "Are you sure you want to delete build/, install/, and log/? [y/N] " confirm
if [[ $confirm == [yY] ]]; then
    sudo rm -rf build/ install/ log/ 
    echo "Directories removed."
else
    echo "Operation cancelled."
fi

read -p "Are you sure you want to delete all packages in src folder? [y/N] " confirm
if [[ $confirm == [yY] ]]; then
    # delete everything under src/ except mysrc/ folders and *.py files (including recursively).
    sudo bash -c 'cd src && find . \( -name "mysrc" -o -name "*.py" \) -prune -o -exec rm -rf {} +'
    echo " Packages removed."
else
    echo "Operation cancelled."
fi

