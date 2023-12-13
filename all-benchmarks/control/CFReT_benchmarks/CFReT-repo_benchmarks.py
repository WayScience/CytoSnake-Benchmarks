#!/usr/bin/env python
# coding: utf-8

# # Benchmark Data Compilation Notebook
#
# In this Notebook, our objective is to compile benchmark data from the `\bulk_benchmarks` and `\single_benchmarks` directories, generating two distinct `.csv` files with raw data.
# These files will serve as datasets for direct comparison with the benchmarks of the CytoSnake workflows.
#

# ## Imports

# In[1]:


import json
import pathlib
import sys
from datetime import datetime

import pandas as pd

sys.path.append("../../../")
from src.benchmark_utils import get_benchmark_files  # noqa

# # Parameters Used in this Notebook
#
# Follow parameters used in this notebook.

# In[2]:


# inputs
working_dir = pathlib.Path().resolve()
benchmark_dir = pathlib.Path("./benchmarks").resolve(strict=True)

# outputs paths
# single_benchmark_csv = working_dir / "single_benchmarks.csv"


# ## Loading all JSON files
#
# Here we are loading all the JSON files.
# The file name structure of the JSON files is `{Plate_name}_{type}_{process}_benchmarks.json`.
# Also we are loading the file size information.

# In[3]:


single_json_files = list(get_benchmark_files(benchmark_dir, ext="json"))

# loading json file that contains file size information
with open("./file_size.json", encoding="utf-8", mode="r") as content:
    plate_size = json.load(content)


# In[4]:


# applying time format
tformat = "%Y-%m-%d %H:%M:%S.%f"

# collecting all data
raw_benchmark_data = []

# iterating each json file and extract data
for single_json_file in single_json_files:
    # collecting data from just file name
    plate_name = single_json_file.stem.split("_CFReT_")[0]
    file_size = plate_size[plate_name]
    process_name = single_json_file.stem.split("_CFReT_")[1].split("_benchmark")[0]

    # opening json file to extract benchmark information
    with open(single_json_file, encoding="utf-8", mode="r") as contents:
        benchmark_data = json.load(contents)

        # accessing to all metadata from benchmarks
        meta_data = benchmark_data["metadata"]
        selected_data = {
            "pid": meta_data["pid"],
            "process_name": process_name,
            "input_data_name": plate_name,
            "start_time": datetime.strptime(meta_data["start_time"], tformat),
            "end_time": datetime.strptime(meta_data["end_time"], tformat),
            "time_duration": (
                datetime.strptime(meta_data["end_time"], tformat)
                - datetime.strptime(meta_data["start_time"], tformat)
            ).total_seconds(),
            "total_allocations": int(meta_data["total_allocations"]),
            "peak_memory": round(int(meta_data["peak_memory"]) / 1024**2, 3),
            "file_size": plate_size[plate_name],
        }

    # append to list
    raw_benchmark_data.append(selected_data)


# In[5]:


# create to dataframe
benchmark_df = pd.DataFrame(raw_benchmark_data)
benchmark_df.to_csv("CFReT_complete_benchmark.csv", index=False)
benchmark_df
