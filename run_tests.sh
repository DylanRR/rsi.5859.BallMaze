#!/bin/bash

# Navigate to the rsi.5859.BallMaze directory
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

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
    deactivate
    exit 1
fi

# Run the selected file
selected_file="${test_files[$((file_number-1))]}"
echo "Running $selected_file..."
python "$selected_file"


# Pause and wait for the user to press Enter to close the terminal
while true; do
    read -r -p "Press Enter to close this test..." input
    if [ -z "$input" ]; then
        break
    fi
done

# Deactivate the virtual environment
deactivate