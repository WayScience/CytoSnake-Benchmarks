# CytoSnake-Benchmarks

Welcome to the `CytoSnake`'s Benchmark Repository, where we conduct version-controlled performance tracking of `CytoSnake`'s workflows.
This repository benchmarks various image-based profiling processing workflows.
We use this repo as a version control system to maintain transparency and track changes in performance.
Below we document our benchmarking process, including the datasets used, configuration files, performance metrics measured, and the selected workflow benchmarked Python notebooks.

## Structure

This repository consists of individual folders, each containing a Jupyter notebook that demonstrates the benchmarking code used for evaluating the performance of CytoSnake workflows.
These notebooks are structured with a naming convention `{datatype}_{workflow-used}.ipynb`.
Within each folder, you'll find a README providing information about the benchmark contents, a `figures` folder containing all the generated plots, `data` folder that contains CSV files that store the raw performance data extracted from the benchmarks and associated configuration files used during benchmark execution.

Below is a table that describes all of the currently available benchmarks:
| Directory Name              | Description                                                                                                                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cell-health-cp-cp_process` | Benchmarks the [`cp_process`](https://cytosnake.readthedocs.io/en/latest/workflows.html#cp-process) workflow using the cell-health [dataset](https://nih.figshare.com/articles/dataset/Cell_Health_-_Cell_Painting_Single_Cell_Profiles/9995672/5) cell profile features |

## Installation and Usage

### Installation

Here's an improved version:

### Installation

To get started, follow these steps:

1. Clone the benchmark repository to your local machine:

   ```bash
   git clone git@github.com:WayScience/CytoSnake.git
   ```

2. Install `CytoSnake` using `bioconda`. It's a good practice to create a dedicated environment for `CytoSnake` to avoid any potential dependency conflicts:

   ```bash
   conda create -n cytosnake
   conda activate cytosnake
   conda install -c bioconda cytosnake
   ```

   > **Note**: Setting up a fresh environment for `CytoSnake` installation is highly recommended to ensure a smooth installation process and prevent any dependency conflicts.

### Instructions on how to run benchmarking

1. Begin by creating a new folder and navigating into it:

   ```bash
   mkdir new_benchmarking_folder && cd new_benchmarking_folder
   ```

2. Copy the notebook template from the `templates` folder into your current directory. Be sure to rename the notebook to match the specific benchmark you're working on, following the naming structure provided above:

   ```bash
   cp ../templates/nb_template.ipynb . && mv nb_template.ipynb new_nb_name.ipynb
   ```

3. **Important**: Set `CytoSnake` into benchmarking mode. If you're unsure how to do this, refer to the [documentation](https://cytosnake.readthedocs.io/en/latest/benchmarking.html) for guidance.

4. Next, proceed to execute the workflow of your choice. You can explore the available workflows [here](https://cytosnake.readthedocs.io/en/latest/workflows.html).

5. Once the workflow has been completed, you'll find a `benchmarks` folder in your directory containing all the raw data. This folder serves as a repository for consolidating and parsing the data using the notebook you've prepared.

6. Execute the notebook by running the following command in your terminal:

   ```bash
   jupyter nbconvert --to notebook --execute --inplace your_notebook.ipynb
   ```

   > **Note**: Ensure to replace `your_notebook.ipynb` with the name of your specific notebook file. This command will execute the notebook in place, updating the existing file with the executed code and results.
