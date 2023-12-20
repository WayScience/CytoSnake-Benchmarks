#!/bin/bash

# exit on first error encountered:
set -e

# Clone the CFReT_data repository
git clone https://github.com/WayScience/CFReT_data.git

# Move into the CFReT_data directory
cd CFReT_data

# Reset the repository to a specific commit hash for reproducibility
git reset --hard 264acc077cd8205cd1b0e327e654bbb22391f9c8

# Download the version of pycytominer used in this pipeline:
pip install git+https://github.com/cytomining/pycytominer@c4de0a9a4fecbf1ad11872bb14c18d24d1b1851

# Move back to the parent directory
cd ..

# Create a directory named 'benchmarks'
mkdir benchmarks

# Change to the '3.process_cfret_features' directory
cd CFReT_data/3.process_cfret_features

# copy the memray script into the directory
cp ../../memray_1.single_cell_processing.py .

# Run the Python script 'memray_1.single_cell_processing.py' located in the parent directory
python memray_1.single_cell_processing.py

# Move all files with the '.bin' extension to the 'benchmarks' directory
mv *.bin ../../benchmarks

# Print a message indicating that the benchmark is complete
echo "Benchmark complete!"
