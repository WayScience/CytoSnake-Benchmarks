# NF1 Data Processing Benchmark

Welcome to the NF1 Data Processing Benchmark repository! This directory provides insights into the performance of the current single-cell processing pipeline available within the [NF1-data-repo](https://github.com/WayScience/nf1_cellpainting_data/tree/main).

## File Directory

| File Name                       | Description                                                   |
|----------------------------------|---------------------------------------------------------------|
| `file_size.json`                 | Contains file size information                                |
| `NF1-repo_benchmarks.ipynb`      | Main notebook that processes the benchmark files              |
| `NF1-repo_benchmark_prep.ipynb`  | Notebook that contains preprocessing steps before executing the main benchmark notebook |
| `bulk_benchmarks`                | Folder containing all benchmark files for bulk datasets        |
| `single_benchmarks`              | Folder containing all benchmark files for single-cell datasets |
| `nf1_complete_benchmark.csv`     | CSV file containing all benchmarks in a structured format      |

## Repository Version

The benchmark was conducted using a specific version of the NF1-data repo. You can find the exact version [here](https://github.com/WayScience/nf1_cellpainting_data/tree/main@46dc73b74c2e995e86a311f91996e3302b98dded).

## Benchmarking Details

The benchmarking process utilized the [`memray`](https://bloomberg.github.io/memray/) tool to assess the [2.pycytominer_singlecell_pipelines.ipynb](https://github.com/WayScience/nf1_cellpainting_data/blob/main/3.processing_features/2.pycytominer_singlecell_pipelines.ipynb) pipeline.
The primary steps conducted by [`pycytominer`](https://github.com/cytomining/pycytominer) included annotation, normalization, and feature selection.
Comprehensive documentation for these processes can be found [here](https://pycytominer.readthedocs.io/en/stable/).

For each step in the pipeline, profiling was performed independently, resulting in benchmark reports named in the format `{plate_name}_nf1_{data-type}_{process}_benchmarks.bin`.
These files contain detailed information on resource usage and runtime.
The individual benchmark reports were then merged into a centralized benchmark file named `nf1_complete_benchmark.csv`.

### Types of benchmarks

Two distinct types of data, classified as `singlecell` and `bulk`, where benchmarked.

There are two folders that contains the benchmarks of the pipeline with the selected datatype:

1. **`single_benchmarks`**: Contains benchmarks associated with the single-cell data processing pipeline.

2. **`bulk_benchmarks`**: Encompasses benchmarks related to the bulk data processing pipeline.
## How to run the benchmarks

To start the benchmark process, execute the shell script:

```bash
# Execute the benchmarking script
./run_benchmarks.sh
```
> **Note**: Before running this script, rename the existing benchmark directories to a different name (e.g., _benchmarks) as the script will create an additional benchmark folder.

Upon completion of the shell script, you should receive a "complete message," with the `bulk_benchmarks` and `single_benchmarks` folders created.
