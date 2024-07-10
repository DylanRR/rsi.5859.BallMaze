#!/bin/bash

# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the project directory
cd "$SCRIPT_DIR"

# Fetch the latest changes from the repository
echo "Fetching the latest changes from the repository..."
if git fetch origin; then
    echo "Successfully fetched the latest changes."
else
    echo "Failed to fetch the latest changes."
    exit 1
fi

# Reset local branch to match the remote branch
echo "Resetting local branch to match the remote branch..."
if git reset --hard origin/main; then
    echo "Successfully reset the local branch."
else
    echo "Failed to reset the local branch."
    exit 1
fi

# Create a virtual environment
echo "Creating a virtual environment..."
if python3 -m venv venv; then
    echo "Virtual environment created successfully."
else
    echo "Failed to create a virtual environment."
    exit 1
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
if pip install -r requirements.txt; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies."
    deactivate
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

# Deactivate the virtual environment
deactivate