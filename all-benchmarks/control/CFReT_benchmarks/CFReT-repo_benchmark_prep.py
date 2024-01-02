#!/usr/bin/env python
# coding: utf-8

# # Benchmark Preparation from NF1 Data Repository
#
# This notebook focuses on the conversion of binarized files generated from Memray into JSON files within the context of the CFReT Data Repository. Furthermore, the notebook generates a JSON file that stores information related to the sizes of input files, allowing for the monitoring of their initial sizes at the start of the workflow.
#
# **Note:** To successfully execute this notebook, it must reside in the [CFReT-data-repo](https://github.com/WayScience/nf1_cellpainting_data), specifically within this [directory](https://github.com/WayScience/CFReT_data/tree/main/3.process_cfret_features). Ensure that the `benchmarks` folder is present in that directory.
#
# The inclusion of this notebook here aims to provide transparency regarding the benchmarking preparations before integrating them into the [CytoSnake-Benchmarks](https://github.com/WayScience/CytoSnake-Benchmarks) repository.

# In[2]:


import json
import pathlib
import subprocess

# ## Setting parameters
#
# This section contains all the parameters used to run this benchmark

# In[4]:


# constants
CWD_PATH = pathlib.Path().resolve(strict=True)

# inputs
DATA_DIR = pathlib.Path("./data/converted_profiles/").resolve(strict=True)
BENCHMARK_DIR = pathlib.Path("./benchmarks/").resolve(strict=True)


# ## Benchmarking Preparation
#
# In this section, we collect information in  regards to file sizes and store it JSON file. Next, we utilize `Memray's` [stats](https://bloomberg.github.io/memray/stats.html) command line tool, leveraging the `subprocess` module, to convert all binary files (bin files) into JSON files.
#
# All processed files are systematically stored within their respective benchmark folders.

# ## Getting input file size
#
# Extracting file size information from the provided directory path and transforming it into a JSON file.

# In[3]:


# get all data files
plate_files = DATA_DIR.glob("*.parquet")

# create a dictionary that contains the plate name and file size in MB
file_size_map = {}
for plate_name in plate_files:
    name = plate_name.stem.split("_converted")[0]
    file_size = plate_name.stat().st_size

    # converting bytes to MegaBytes
    file_size_map[name] = round(file_size / 1024**2, 3)

# writing out json file containing file size info
with open("file_size.json", encoding="utf-8", mode="w") as stream:
    json.dump(file_size_map, stream, indent=4)


# ### Converting all `.bin` into `.json` files
#
# Converting all bin files into json files.

# In[4]:


# converting all single benchmark files into json
for bin_path in BENCHMARK_DIR.glob("*.bin"):
    json_out = BENCHMARK_DIR / f"{bin_path.stem}.json"

    # # executing memray to convert bin files into json files
    print(
        " ".join(
            [
                "memray",
                "stats",
                "--json",
                "--output",
                str(json_out),
                "--force",
                str(bin_path),
            ],
        )
    )
    memray_stats = subprocess.run(
        [
            "memray",
            "stats",
            "--json",
            "--output",
            str(json_out),
            "--force",
            str(bin_path),
        ],
        capture_output=True,
        check=True,
    )

    # stdout message
    print(
        f"{bin_path.relative_to(CWD_PATH)} was successfully converted into {json_out.relative_to(CWD_PATH)}"
    )
