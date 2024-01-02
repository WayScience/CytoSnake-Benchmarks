# CFReT Data Processing Benchmark

Welcome to the CFReT Data Processing Benchmark repository! This directory provides insights into the performance of the current single-cell processing pipeline available within the [CFReT-data-repo](https://github.com/WayScience/CFReT_data).

## File Directory

| File Name                       | Description                                                   |
|----------------------------------|---------------------------------------------------------------|
| `file_size.json`                 | Contains file size information                                |
| `CFReT-repo_benchmarks.ipynb`      | Main notebook that processes the benchmark files              |
| `CFReT-repo_benchmark_prep.ipynb`  | Notebook that contains preprocessing steps before executing the main benchmark notebook |
| `benchmarks`                     | Folder containing all benchmarks for CFReT dataset            |
| `CFReT_complete_benchmark.csv`     | CSV file containing all benchmarks in a structured format     |

## Repository Version

The benchmark was conducted using a specific version of the CFReT-data repo.
You can find the exact version [here](https://github.com/WayScience/CFReT_data@e7b9637b17345c3a0378f3224b121bb8285fbef1).

## Benchmarking Details

The benchmarking process utilized the [`memray`](https://bloomberg.github.io/memray/) tool to assess the [2.pycytominer_singlecell_pipelines.ipynb](https://github.com/WayScience/nf1_cellpainting_data/blob/main/3.processing_features/2.pycytominer_singlecell_pipelines.ipynb) pipeline.
The primary steps conducted by [`pycytominer`](https://github.com/cytomining/pycytominer) included annotation, normalization, and feature selection.
Comprehensive documentation for these processes can be found [here](https://pycytominer.readthedocs.io/en/stable/).

For each step in the pipeline, profiling was performed independently, resulting in benchmark reports named in the format `{plate_name}_nf1_{data-type}_{process}_benchmarks.bin`.
These files contain detailed information on resource usage and runtime.
The individual benchmark reports were then merged into a centralized benchmark file named `nf1_complete_benchmark.csv`.

## How to run the benchmarks

To start the benchmark process, execute the shell script:

```bash
# Execute the benchmarking script
./run_benchmarks.sh
```
> **Note**: Before running this script, rename the existing benchmark directory to a different name (e.g., _benchmarks) as the script will create an additional benchmark folder.

Upon completion of the shell script, you should receive a "complete message," and a new `benchmarks` folder will be created.
