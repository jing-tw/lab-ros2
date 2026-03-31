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

read -p "Are you sure you want to delete everything in src except python source files/? [y/N] " confirm
if [[ $confirm == [yY] ]]; then
    # sudo rm -rf src/
    cd src && find . \( ! -name 'old' -a ! -name '*.py' \) -prune -o -exec rm -rf {} +
    echo "Directories removed."
else
    echo "Operation cancelled."
fi

