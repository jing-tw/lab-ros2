#!/bin/bash
docker compose down  
docker compose down --rmi all 

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
    # delete everything under src/ except old/ folders and *.py files (including recursively).
    sudo bash -c 'cd src && find . \( -name "old" -o -name "*.py" \) -prune -o -exec rm -rf {} +'
    echo "Directories removed."
else
    echo "Operation cancelled."
fi

