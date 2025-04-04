#!/bin/bash

# Display the title before execution
echo "===================================="
echo "  Agentic AI Workflow Automation  "
echo "===================================="

# Create the responses directory if it does not exist
mkdir -p responses

# Prompt user for global_task and output file name
read -p "Enter the task: " global_task
read -p "Enter the output file name (with .txt extension): " output_file

# Define the full path for the output file
output_path="$output_file"

# Run the Python scripts with user inputs
python script.py "$global_task" "$output_path" | python filter.py > "$output_path"

echo "Execution completed. Output saved to $output_path"

# Open the output file in Notepad (Windows Only)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    notepad.exe "$output_path"
else
    echo "Notepad is only available on Windows. Please open $output_path manually."
fi
