#!/bin/bash
# kill_python_processes.sh

# Must run: chmod +x kill_python_processes.sh to make the script executable
# To run: sudo ./kill_python_processes.sh

# Find all Python processes and terminate them
ps aux | grep '[p]ython' | awk '{print $2}' | xargs sudo kill -9