# Cell-health CellProfiler features with `cp_process`

## Introduction

Here, we benchmark the `cp_process_singlecells` workflow with the NF1 dataset [dataset](https://github.com/WayScience/nf1_cellpainting_data) that is demonstrated in the jupyter notebook.

## About the data

The NF1 data repository, available at [https://github.com/WayScience/nf1_cellpainting_data](https://github.com/WayScience/nf1_cellpainting_data), houses image-based profiles assayed through CellPainting. This dataset comprises information from four plates, each annotated with metadata corresponding to specific genotypes. Genotypes are categorized as wild type (+/+) and Null (-/-).

For a more understanding of the dataset and its intricacies, please refer to the [NF1 repository](https://github.com/WayScience/nf1_cellpainting_data).

## Files

In the benchmark workflow, you'll find the following types of files and directories:

- `csv` files, which store the collected performance data.
- The `benchmark/` directory contains benchmark files in `.json` format.