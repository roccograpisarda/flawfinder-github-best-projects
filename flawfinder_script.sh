#!/bin/bash

echo "=============|Script Started|============="

# Get the directory of the script
base_dir=$(dirname -- "$0")

# Projects directory containing the project directories
projects_dir="$base_dir/projects"

# Output directory for CSV files
output_dir="$base_dir/output"

# Calculate the absolute path of the output directory
output_dir=$(realpath "$output_dir")

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Create the projects directory if it doesn't exist
mkdir -p "$projects_dir"

# Clone the repositories only if the project directories don't exist
clone_if_not_exists() {
    local repo_url=$1
    local repo_name=$2
    local repo_dir="$projects_dir/$repo_name"

    if [ ! -d "$repo_dir" ]; then
        echo "Clonining $repo_name..."
        git clone "$repo_url" "$repo_dir"
    else
        echo "Skipping clone: $repo_name already exists"
    fi
}
echo "=============|Cloning Repositories|============="
# Clone the repositories
clone_if_not_exists "https://github.com/Genymobile/scrcpy.git" "scrcpy"
clone_if_not_exists "https://github.com/obsproject/obs-studio.git" "obs-studio"
clone_if_not_exists "https://github.com/videolan/vlc.git" "vlc"
echo "=============|Starting Flawfinder|============="
# Iterate over each project directory
for project_dir in "$projects_dir"/*; do
    if [[ -d "$project_dir" ]]; then
        # Extract the project name from the directory path
        project_name=$(basename "$project_dir")

        echo "Processing project: $project_name"

        # Execute the flawfinder command and redirect the output to a CSV file
        flawfinder --minlevel 4 --csv "$project_dir/". > "flawfinder_output.csv"

        # Move the CSV file to the output directory if it exists
        if [ -d "$output_dir" ]; then
            mv "flawfinder_output.csv" "$output_dir/$project_name.csv"
        else
            echo "Output directory does not exist: $output_dir"
        fi

        # Return to the base directory
        cd "$base_dir" || exit
    fi
done

echo "=============|Creating Plots|============="
python3 script.py
