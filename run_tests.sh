#!/bin/bash

# Navigate to the rsi.5859.BallMaze directory
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

while true; do
    # List all .py files in the tests folder
    echo "Available test files:"
    test_files=(tests/*.py)
    if [ ${#test_files[@]} -eq 0 ]; then
        echo "No test files found in the tests folder."
        deactivate
        exit 1
    fi

    for i in "${!test_files[@]}"; do
        echo "$((i+1)). ${test_files[$i]}"
    done

    # Prompt the user to select a file
    read -p "Enter the number of the test file you want to run: " file_number

    # Validate the user input
    if ! [[ "$file_number" =~ ^[0-9]+$ ]] || [ "$file_number" -lt 1 ] || [ "$file_number" -gt ${#test_files[@]} ]; then
        echo "Invalid selection."
        continue
    fi

    # Run the selected file with sudo
    selected_file="${test_files[$((file_number-1))]}"
    echo "Running $selected_file with sudo..."
    sudo python "$selected_file"

    # Prompt the user to either run another test or exit
    while true; do
        read -r -p "Do you want to run another test? (yes/no): " choice
        if [ "$choice" == "yes" ]; then
            break
        elif [ "$choice" == "no" ]; then
            deactivate
            exit 0
        else
            echo "Invalid choice. Please enter 'yes' or 'no'."
        fi
    done
done