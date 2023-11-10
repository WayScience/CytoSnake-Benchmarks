#!/usr/bin/env python
# coding: utf-8

# # Cell-Health CP feature with CytoSnake's `cp_process` Wortkflow Benchmarking Notebook.
# 
# This study focuses on benchmarking CytoSnake's cp_process workflow using the Cell-Health dataset. We assess the workflow's performance in terms of time, memory allocation, and memory usage to provide a detailed understanding of its efficiency.
# 
# Development of this notebook has been heavily influced by `CytoTable-Benchmark` [repo](https://github.com/cytomining/CytoTable-benchmarks/blob/main/notebooks/cytotable_and_pycytominer_analysis.ipynb) developed by [Dave Bunten](https://github.com/d33bs)

# In[1]:


import sys
import pathlib
import shutil
import subprocess
import json
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append("..")
from src.common import get_benchmark_files, create_filename_path_mapping

warnings.filterwarnings("ignore")


# ## Parameters
# 
# Below are the list of parameters used in this notebook
# 

# In[2]:


# inputs
CWD_PATH = pathlib.Path(".").resolve(strict=True)
BENCHMARK_DIR_PATH = pathlib.Path("./benchmarks").resolve(strict=True)
README_PATH = pathlib.Path("./README.md").resolve(strict=True)
DATA_DIR = pathlib.Path("./data").resolve()

# outputs
IMAGE_DIR = pathlib.Path("images")
IMAGE_DIR.mkdir(exist_ok=True)


# ## Converting binary files into json files
# 
# In this section, we will focus on converting the memory output files from binary (`.bin`) format to JSON files. 
# These files hold the raw calculations generated during the benchmarking process. To begin, we use the `get_all_bin_files()` to locate all binarized files. The we use the `memray stats` process to convert the `.bin` files into `.json` files iteratively.
# The resulting JSON file will provide a structured representation of the data, making it more accessible and suitable for analysis.

# In[3]:


# check if memray is installed
if shutil.which("memray") is None:
    raise FileNotFoundError("Unable to locate 'memray' executable")


# iterate all bin files an convert to json files
for bin_path in get_benchmark_files(BENCHMARK_DIR_PATH, ext="bin"):
    json_out = BENCHMARK_DIR_PATH / f"{bin_path.stem}.json"

    # # executing memray to convert bin files into json files
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


# ## Merging all JSON file data into a single CSV file 
# 
# In the section, we aim to consolidate data from multiple JSON files into a single CSV file. 
# This process involves extracting specific data from each JSON file and structuring it into a CSV table. 
# The CSV format provides a straightforward, tabular structure for easy analysis, simplifying data handling.

# In[4]:


# format for memray time strings
tformat = "%Y-%m-%d %H:%M:%S.%f"

# creating a list where all the data will be stored
raw_benchmark_data = []

# create a for loop iterating all json files and extract data
for json_file in get_benchmark_files(BENCHMARK_DIR_PATH, ext="json"):
    # open json file
    with open(json_file, mode="r", encoding="utf-8") as contents:
        memray_data = json.load(contents)

    # get name of sqlite file or input file
    json_file_name = json_file.name.split("_")

    # this assumes that all file were used as an input
    if len(json_file_name) == 2 or json_file_name[0] == "feature":
        name = "all_inputs"
    elif len(json_file_name) >= 3:
        # get the input file name from {inputname}_{script_name}_benchmark.json
        name = json_file.name.rsplit("_", 2)[0]

    # extract required data
    meta_data = memray_data["metadata"]
    script_name = pathlib.Path(meta_data["command_line"]).name.split(".", 1)[1]
    selected_data = {
        "pid": meta_data["pid"],
        "script": script_name,
        "input_data_name": f"{name}_{script_name.split('.')[0]}"
        if name == "all_inputs"
        else name,
        "start_time": datetime.strptime(meta_data["start_time"], tformat),
        "end_time": datetime.strptime(meta_data["end_time"], tformat),
        "time_duration": (
            datetime.strptime(meta_data["end_time"], tformat)
            - datetime.strptime(meta_data["start_time"], tformat)
        ).total_seconds(),
        "total_allocations": int(meta_data["total_allocations"]),
        "peak_memory": int(meta_data["peak_memory"]) / 1024**2,
    }

    # append to list
    raw_benchmark_data.append(selected_data)

# create dataframe
benchmark_df = pd.DataFrame(raw_benchmark_data)
benchmark_df.to_csv("complete_benchmark.csv", index=False)
benchmark_df


# In[5]:


# next step is to add file size data into the benchmark DF
def get_file_size(fname: str, f_mapping: dict) -> float | None:
    """Gets file size when given a file path

    Parameters
    ----------
    fname : str
        file_name
    f_mapping : dict
        dict containing absolute path of the file

    Returns
    -------
    float|None
        returns the file size of the file.
    """
    # search in map
    path = f_mapping[fname]

    # return None if not found
    if path is None:
        return None

    # return file size
    return round((pathlib.Path(path).stat().st_size / 1024**2), 3)


# create mapping
input_names = benchmark_df["input_data_name"].unique()
mapping = create_filename_path_mapping(
    input_names, data_dir=DATA_DIR, data_ext="sqlite"
)

# adding file file size information into dataframe
benchmark_df["file_size"] = benchmark_df["input_data_name"].apply(
    get_file_size, f_mapping=mapping
)
benchmark_df


# ## Workflow perfroamnce per input.
# Here we are looking at the performance of the workflow per input. Here we are seeing how the workflow handles the data. Here we are checking how much time, resources and memory peak the whole workflow took when analyzing one single sqlite file. 

# In[6]:


# group the data frame based on their process input_data_name
# this demonstrates 1 inputs in all scripts (emulating a snigle process of the workflow
group_by_input = benchmark_df.groupby(by=["input_data_name"])


workflow_per_input_data = []
for name, df in group_by_input:
    workflow_per_input_data.append(
        [
            name[0],
            df["file_size"].unique()[0],
            df["peak_memory"].max(),
            df["total_allocations"].sum(),
            df["time_duration"].sum(),
        ]
    )


columns = [
    "input_name",
    "file_size",
    "peak_memory",
    "total_allocation",
    "time_duration",
]
workflow_per_input_df = pd.DataFrame(workflow_per_input_data, columns=columns)
workflow_per_input_df.to_csv("workflow_per_input_performance.csv", index=False)
workflow_per_input_df


# ## Total Allocations used 
# 
# The total amount of allocations refers to the count of memory allocations operations performed by the workflow. This occurs when a program requests and receives memory from the system memory management system. Therefore, it captures the cumulative amount of dynamically allocated memory in a program, providing insights into its memory footprint and resource management efficiency.

# In[7]:


# Sample data (replace with your own data)
input_names = workflow_per_input_df.input_name
total_allocations = workflow_per_input_df.total_allocation
peak_memory = workflow_per_input_df.peak_memory

fig = px.bar(
    workflow_per_input_df,
    x="input_name",
    y="peak_memory",
    text="peak_memory",
    hover_data=["total_allocation"],
    color="total_allocation",
    template="simple_white",
    barmode="relative",
    labels={"total_allocation": "N_Allocations"},
)
fig.update_traces(texttemplate="%{text:.2f} MB", textposition="outside")
fig.update_layout(
    title="Peak Memory Usage and Total Allocations per Input",
    xaxis_title="Input Name",
    yaxis_title="Peak Memory Usage (MB)",
)
fig.show()

# print out plot
fig.write_image("images/peak_memory_total_allocations.png")


# > **Figure 1**: This figure illustrates the memory usage and total allocations calculated per input dataset. The prefix 'all_inputs' indicates that all plate files were utilized in the execution of this process. Each bar's height corresponds to the peak memory usage of these files, while the color spectrum signifies the number of allocations made by the process throughout the entire workflow execution.

# ## Memory usage and runtime
# 
# Here, we assess the performance of `cp_process` in terms of memory utilization and runtime. This analysis results in three distinct plots:
# 
# 1. Peak memory usage for each step.
# 2. Runtime for each step.
# 3. Runtime per input in each step."
# 
# 

# In[8]:


## Peak memory usage per step
group_by_step = benchmark_df.groupby(by=["script"])


collected_data = []
for name, df in group_by_step:
    data = [
        name[0].replace(".py", ""),
        df["peak_memory"].sum(),
        df["time_duration"].max(),  # longest time is the limiting factor
    ]

    collected_data.append(data)

columns = ["process_name", "peak_memory", "time_duration"]
step_df = pd.DataFrame(collected_data, columns=columns)

step_df


# In[9]:


# plot into line graph (memory usage vs step process)

# changing the order to the process to correctly align with cp_process
correct_order = [
    "aggregate_cells",
    "annotate",
    "normalize",
    "feature_select",
    "consensus",
]
plot_df = step_df[step_df["process_name"].isin(correct_order)]
plot_df = plot_df.set_index("process_name").loc[correct_order].reset_index()
plot_df

# Create a line graph for peak memory
annotations = [
    go.layout.Annotation(
        text=f"Total run time: {round(step_df['time_duration'].sum()/60, 2)}"
    )
]

fig1 = px.line(
    plot_df,
    x="process_name",
    y="peak_memory",
    title="Peak Memory Per Process (all inputs used)",
    labels={"process_name": "Step", "peak_memory": "Peak Memory (MB)"},
    template="simple_white",
)
fig1.update_traces(line=dict(color="red"))
fig1.add_annotation(
    text=f"<b>Peak memory usage: {round(step_df['peak_memory'].max(), 2)} MB</b>",
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.9,
    showarrow=False,
)

# Create a line graph for time duration
fig2 = px.line(
    plot_df,
    x="process_name",
    y="time_duration",
    title="Time Duration Per Process (all inputs used)",
    labels={"process_name": "Step", "time_duration": "Time Duration (Sec)"},
    template="simple_white",
)
fig2.update_traces(line=dict(color="blue"))
fig2.add_annotation(
    text=f"<b>Total run time: {round(step_df['time_duration'].sum()/60, 2)} min</b>",
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.9,
    showarrow=False,
)

# display line plots
fig1.show()
fig2.show()

# write out images
fig1.write_image("images/peak_memory_per_process.png")
fig2.write_image("images/time_duration_per_process.png")


# > **Figure 2**: This figure provides an insight into the performance of the `cp_process` in CytoSnake, considering memory usage and run time for each step. The top graph depicts the memory usage per step using all available inputs, with the peak memory usage remaining under 4GB. The bottom graph displays the total runtime per step for the entire workflow, revealing that the `aggregation` step consumes the majority of the execution time. 

# In[10]:


# generating the multi line plots that represents runtime per input in each step
def clean_script_name(script_name: str) -> str:
    return script_name.split(".")[0]


# Create the plot with Plotly Express
multi_line_df = benchmark_df[
    ["input_data_name", "script", "time_duration", "file_size"]
]

single_input = multi_line_df.loc[multi_line_df["file_size"].isnull()]
single_input["script"] = single_input["script"].apply(clean_script_name)

parallel_input = multi_line_df.loc[~multi_line_df["file_size"].isnull()]
parallel_input["script"] = parallel_input["script"].apply(clean_script_name)
group_par_dfs = parallel_input.groupby(by=["input_data_name"])


columns = ["input_name", "aggregate_cells", "annotate", "normalize", "file_size"]
raw_data = []

for name, df in group_par_dfs:
    # Create a new column with the sorting order
    custom_order = ["aggregate_cells", "annotate", "normalize"]
    df["sorting_order"] = df["script"].apply(lambda x: custom_order.index(x))

    # Sort the DataFrame based on the sorting order
    df = df.sort_values(by="sorting_order", ascending=True)

    # Drop the temporary sorting_order column if needed
    df = df.drop(columns="sorting_order")

    name = [name[0]]
    time_duration = [time for time in df["time_duration"]]
    file_size = [df["file_size"].max()]

    raw_data.append(name + time_duration + file_size)


# minor edits to add array based inputs for example using all plates an a single input
temp_df = pd.DataFrame(raw_data, columns=columns)
all_steps_df = temp_df[["input_name", "aggregate_cells", "annotate", "normalize"]]
all_steps_df["feature_select"] = single_input[
    single_input["script"].isin(["feature_select"])
]["time_duration"].iloc[0]
all_steps_df["consensus"] = single_input[single_input["script"].isin(["consensus"])][
    "time_duration"
].iloc[0]
all_steps_df["file_size"] = temp_df["file_size"]
all_steps_df.to_csv("runtime_per_input_each_step.csv", index=False)
all_steps_df


# In[11]:


# Assign colors corresponding to file size
colors = np.linspace(0, 1, len(all_steps_df))
color_scale = (
    px.colors.cmocean.thermal
)  # You can choose another color scale if you prefer

# Create a Plotly figure with a line plot for each row and color mapping
fig = go.Figure()

for index, row in all_steps_df.iterrows():
    color = color_scale[int(colors[index] * (len(color_scale) - 1))]
    fig.add_trace(
        go.Scatter(
            x=all_steps_df.columns[
                1:-1
            ],  # Exclude "input_name" and "file_size" columns from X values
            y=row[1:-1],  # Exclude "input_name" and "file_size" values from Y
            mode="lines+markers",
            name=row["input_name"],
            line=dict(color=color),
        )
    )

# Customize the layout
fig.update_layout(
    title="Time Duration Per Input Each Step",
    xaxis_title="Steps",
    yaxis_title="Time Duration (sec)",
    template="simple_white",
)

# Show the plot
fig.show()
fig.write_image("images/time_durration_per_input_each_step.png")


# > **Figure 3** : Multiline plots representing the time duration of each step for individual inputs. Each line plot corresponds to a single input, and the y-axis represents the amount of time passed during the execution of each step

# ## Looking at time and File size
# 
# Here we are exploring  the direct relationship between time, file size, and memory utilization in the 'cp_process' workflow of CytoSnake. This analysis aims to establish a quantitative connection between these variables, providing a clearer understanding of how they impact the workflow's performance and resource utilization.

# In[12]:


## Here we are creatingj
time_size_df = workflow_per_input_df.dropna().sort_values(
    by=["time_duration"], ascending=False
)
time_size_df


# In[13]:


# plotting using input file name and time duration as our X and Y and peak memory
# as the additional variable
fig = px.bar(
    time_size_df,
    x="input_name",
    y="time_duration",
    color="peak_memory",
    text="peak_memory",
    labels={
        "input_name": "Input Name",
        "time_duration": "Time Duration",
        "peak_memory": "Peak Memory Usage",
    },
)
fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

fig.update_layout(
    title="Time Duration vs. Input Name with Peak Memory Usage",
    xaxis_title="Plate Name",
    yaxis_title="Time Duration (secs)",
    legend_title="Peak Memory (MB)",
    barmode="relative",
    template="simple_white",
)

fig.show()

# save plot
fig2.write_image("images/time_durration_and_size.png")


# > Figure 4: This bar graph illustrates the relationship between `Time Duration` and `Peak Memory Usage` for different input datasets `Plate Name`. Each bar represents the time duration of a specific dataset, with the color indicating the corresponding peak memory usage. The legend displays the scale of peak memory values, while the x-axis represents the input names. 
