#!/bin/bash

# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the project directory
cd "$SCRIPT_DIR"

# Pull the latest changes from the repository
echo "Pulling the latest changes from the repository..."
if git pull origin main; then
    echo "Successfully pulled the latest changes."
else
    echo "Failed to pull the latest changes."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
if pip3 install -r requirements.txt; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies."
    exit 1
fi

# Indicate that the setup was completed successfully
echo "Setup completed successfully."

# Pause and wait for the user to press Enter to close the terminal
echo "Press Enter to close this window..."
while true; do
    read -r -p "Press Enter to close this window..." input
    if [ -z "$input" ]; then
        break
    fi
done