# Cell-health CellProfiler features with `cp_process`

## Introduction

Here, we benchmark the `cp_process`` workflow with the Cell-Health [dataset](https://nih.figshare.com/articles/dataset/Cell_Health_-_Cell_Painting_Single_Cell_Profiles/9995672/5) that is demonstrated in the jupyter notebook.

## About the data

The Cell-Health dataset comprises data from nine plates, where cell assays were conducted using Cell Painting and the resulting measurements were quantified using CellProfiler.
This project involved the collection of Cell Painting measurements from CRISPR experiments that targeted a specific set of 59 genes across three distinct cell lines: [A549](https://www.cellosaurus.org/CVCL_0023), [ES2](https://www.cellosaurus.org/CVCL_AX39), and [HCC44](https://www.cellosaurus.org/CVCL_2060).
In total, the dataset amounts to  130GB of raw data, all of which has undergone processing using `CytoSnake`'s `cp_process` workflow.

## Files

In the benchmark workflow, you'll find the following types of files and directories:

- `csv` files, which store the collected performance data.
- The `images/` directory, where all plots are stored.
- The `benchmark/` directory contains benchmark files in `.json` format.
