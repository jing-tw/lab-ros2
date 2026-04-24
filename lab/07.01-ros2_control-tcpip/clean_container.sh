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

# === Whitelist-based cleanup for src/ with glob support ===
read -p "Are you sure you want to delete all files/folders in src/ except whitelisted items? [y/N] " confirm
if [[ $confirm == [yY] ]]; then
    # Whitelist supports exact names AND glob patterns
    KEEP_LIST=("my*" "*.py" "README.md" ".git" "*.json")

    # Build find expression using -o between each pattern
    FIND_EXPR=""
    for pattern in "${KEEP_LIST[@]}"; do
        [[ -n $FIND_EXPR ]] && FIND_EXPR="$FIND_EXPR -o "
        FIND_EXPR="$FIND_EXPR -name \"$pattern\""
    done

    echo "Keeping patterns: ${KEEP_LIST[*]}"
    echo "Deleting everything else in src/..."

    # Dry run first - comment this out when you're ready
    echo "DRY RUN - would delete:"
    bash -c "cd src && find . -mindepth 1  \\( $FIND_EXPR \\) -prune -o -print"

    read -p "Proceed with actual delete? [y/N] " confirm2
    if [[ $confirm2 == [yY] ]]; then
        sudo bash -c "cd src && find . -mindepth 1  \\( $FIND_EXPR \\) -prune -o -exec rm -rf {} +"
        echo "Cleanup done."
    else
        echo "Delete cancelled."
    fi
else
    echo "Operation cancelled."
fi
