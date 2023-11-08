# CytoSnake-Benchmarks

Welcome to the `CytoSnake`'s Benchmark Repository, where we conduct version-controlled performance tracking of `CytoSnake`'s workflows.
This repository benchmarks various image-based profiling processing workflows.
We use this repo as a version control system to maintain transparency and track changes in performance.
Below we document our benchmarking process, including the datasets used, configuration files, performance metrics measured, and the selected workflow benchmarked Python notebooks.

## Structure

This repository consists of individual folders, each containing a Jupyter notebook that demonstrates the benchmarking code used for evaluating the performance of CytoSnake workflows.
These notebooks are structured with a naming convention `{datatype}_{workflow-used}.ipynb`.
Within each folder, you'll find a README providing information about the benchmark contents, a `figures` folder containing all the generated plots, `data` folder that contains CSV files that store the raw performance data extracted from the benchmarks and associated configuration files used during benchmark execution.

Below is a table that describes all of the currently available benchmarks inside the `all-benchmarks` directory:
| Directory Name              | Description                                                                                                                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cell-health-cp-cp_process` | Benchmarks the [`cp_process`](https://cytosnake.readthedocs.io/en/latest/workflows.html#cp-process) workflow using the cell-health [dataset](https://nih.figshare.com/articles/dataset/Cell_Health_-_Cell_Painting_Single_Cell_Profiles/9995672/5) cell profile features |

## Installation and Usage

### Installation

To get started, follow these steps:

1. Clone the benchmark repository to your local machine:

   ```bash
   git clone git@github.com:WayScience/CytoSnake-Benchmarks.git
   ```

2. Install `CytoSnake` using `bioconda`. It's a good practice to create a dedicated environment for `CytoSnake` to avoid any potential dependency conflicts:

   ```bash
   conda create -n cytosnake
   conda activate cytosnake
   conda install -c bioconda cytosnake
   ```

   > **Note**: Setting up a fresh environment for `CytoSnake` installation is highly recommended to ensure a smooth installation process and prevent any dependency conflicts.

   If you have mamba installed, you can replace `conda` with mamba.

## Creating a benchmark

To create a benchmark, follow these steps: First, create a folder in the `all-benchmarks/` directory with the structure `{data_type}_{features}_benchmarks/` for the file name.
Next, transfer all the necessary files into this folder, which should include the benchmark generated when executing CytoSnake's benchmarking mode.
Utilize notebooks to document and display all the raw code and figures generated during the benchmarking analysis.
Lastly, it's recommended to store all intermediate files and figures in the repository, allowing others to review and access them.