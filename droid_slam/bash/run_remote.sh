#!/bin/bash

# Set variables
if [[ $1 =~ ^(-p|--project_path) ]]
then
    project_path=$2
fi

if [[ $5 =~ ^(-s|--server_ip) ]]
then
    server_ip=$6
fi

user=$4 
env=$8

# Copy video to server
echo "Project path is $project_path"
echo "Copying file..."
scp -r ./tmp $user@$server_ip:$project_path/
echo "Copy process finished..."

# Extracting frames and running droid-slam
ssh $user@$server_ip ". ~/.zshrc; cd $project_path; conda activate $env; echo "Starting frame extraction..."; python3 ./utils/extract_frames_ffmpeg.py; echo "Frame extraction completed..."; mkdir $project_path/tmp/output; echo "Running droid-slam..."; python3 demo.py --imagedir=$project_path/tmp/frames --calib=./calib/gopro.txt --reconstruction_path=$project_path/tmp/output; echo "Droid-slam completed...""

# Fetch results
mkdir ./results
scp "$user@$server_ip:$project_path/tmp/output/*.ply" ./results

# Remove tmp folder from server
#ssh $server_ip rm -r $project_path/tmp

# Visualize and remove outlier
python3 outlier_removal.py; python3 vis.py
