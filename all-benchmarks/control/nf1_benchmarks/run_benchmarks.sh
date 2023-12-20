#!/bin/bash

# exit on first error encountered:
set -e

# Clone the CFReT_data repository
git clone https://github.com/WayScience/nf1_cellpainting_data.git

# Move into the CFReT_data directory
cd nf1_cellpainting_data

# Reset the repository to a specific commit hash for reproducibility
git reset --hard 46dc73b74c2e995e86a311f91996e3302b98dded

# Download the version of pycytominer used in this pipeline:
pip install git+https://github.com/cytomining/pycytominer@c4de0a9a4fecbf1ad11872bb14c18d24d1b1851e

# Move back to the parent directory
cd ..

# Create a directory named 'benchmarks'
mkdir bulk_benchmarks && mkdir single_benchmarks

# Change to the '3.process_features' directory
cd nf1_cellpainting_data/3.processing_features

# copy the memray script into the directory
cp ../../memray_1.pycytominer_bulk_pipelines.py . && cp ../../memray_2.pycytominer_singlecell_pipelines.py .

# execute bulk benchmarking and move to bulk_benchmark
python memray_1.pycytominer_bulk_pipelines.py
mv *.bin ../../bulk_benchmarks

# execute single cell benchmarking and move to single_benchmark
python memray_2.pycytominer_singlecell_pipelines.py
mv *.bin ../../single_benchmarks

# Print a message indicating that the benchmark is complete
echo "Benchmark complete!"
