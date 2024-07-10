#!/bin/bash

# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the project directory
cd "$SCRIPT_DIR"

while true; do
    # Ask the user whether to perform a pull or a hard reset
    echo "Do you want to perform a 'pull' or a 'hard reset'? (Enter 'pull' or 'reset')"
    read -r -p "Choice: " choice

    if [ "$choice" == "pull" ]; then
        echo "Pulling the latest changes from the repository..."
        if git pull origin main; then
            echo "Successfully pulled the latest changes."
            break
        else
            echo "Failed to pull the latest changes."
            exit 1
        fi
    elif [ "$choice" == "reset" ]; then
        echo "Warning: Performing a hard reset will cause this script to lose its executable permission."
        read -r -p "Do you want to continue? (yes/no): " confirm
        if [ "$confirm" == "yes" ]; then
            echo "Resetting local branch to match the remote branch..."
            if git reset --hard origin/main; then
                echo "Successfully reset the local branch."
                echo "You will need to run 'chmod +x setup.sh' to make this script executable again."
                break
            else
                echo "Failed to reset the local branch."
                exit 1
            fi
        else
            echo "Returning to the choice between 'pull' and 'reset'."
        fi
    else
        echo "Invalid choice. Please enter 'pull' or 'reset'."
    fi
done

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment..."
    if python3 -m venv venv; then
        echo "Virtual environment created successfully."
    else
        echo "Failed to create a virtual environment."
        exit 1
    fi
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
while true; do
    read -r -p "Press Enter to close this window..." input
    if [ -z "$input" ]; then
        break
    fi
done

# Deactivate the virtual environment
deactivate