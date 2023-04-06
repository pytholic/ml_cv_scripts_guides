#!/bin/bash

# Set variables
# if [[ $1 =~ ^(-p|--project_path) ]]
# then
#     project_path=$2
# fi

project_path=$2
env=$4
cam=$6

# # Copy video to server
# echo "Project path is $project_path"
# echo "Copying file..."
cp -r ./tmp $project_path/
# echo "Copy process finished..."

# Extracting frames and running droid-slam
cd $project_path; conda activate $env; echo "Starting frame extraction..."; python3 utils/extract_frames_ffmpeg.py -d $cam; echo "Frame extraction completed...";
mkdir $project_path/tmp/output; echo "Running droid-slam..."; python3 demo.py --imagedir=$project_path/tmp/frames --calib=./calib/$cam.txt --reconstruction_path=$project_path/tmp/output; echo "Droid-slam completed..."

mkdir $project_path/utils/bash_utils/results
cp $project_path/tmp/output/*.ply $project_path/utils/bash_utils/results
cd $project_path/utils/bash_utils/
# Visualize and remove outlier

python3 outlier_removal.py
python3 vis.py
conda deactivate
