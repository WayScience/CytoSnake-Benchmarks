"""
This script comes the notebook `1.single_cell_processing.ipynb` but this version will contain the memory implementation of it.
This means sp
"""
#!/usr/bin/env python
# coding: utf-8

# # Process single cell profiles

# In[1]:


import pathlib
import pprint

import memray
import pandas as pd
from pycytominer import annotate, feature_select, normalize

# In[2]:


# Path to dir with nuclei feature files
converted_dir = pathlib.Path("./data/converted_profiles")

# output path for single cell profiles
output_dir = pathlib.Path("./data/single_cell_profiles")
output_dir.mkdir(parents=True, exist_ok=True)

# Extract the plate names from the file name
plate_names = [
    file.stem.replace("_converted", "") for file in converted_dir.glob("*.parquet")
]

# path for platemap directory
platemap_dir = pathlib.Path("../metadata/")

# operations to perform for feature selection
feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]


# In[3]:


# create plate info dictionary
plate_info_dictionary = {
    name: {
        "profile_path": str(
            pathlib.Path(
                list(converted_dir.rglob(f"{name}_converted.parquet"))[0]
            ).resolve(strict=True)
        ),
        "platemap_path": str(
            pathlib.Path(list(platemap_dir.rglob(f"{name}_platemap.csv"))[0]).resolve(
                strict=True
            )
        ),
    }
    for name in plate_names
}

# view the dictionary to assess that all info is added correctly
pprint.pprint(plate_info_dictionary, indent=4)


# In[4]:


for plate, info in plate_info_dictionary.items():
    print(f"Performing pycytominer pipeline for {plate}")
    output_annotated_file = str(
        pathlib.Path(f"{output_dir}/{plate}_sc_annotated.parquet")
    )
    output_normalized_file = str(
        pathlib.Path(f"{output_dir}/{plate}_sc_normalized.parquet")
    )
    output_feature_select_file = str(
        pathlib.Path(f"{output_dir}/{plate}_sc_feature_selected.parquet")
    )

    profile_df = pd.read_parquet(info["profile_path"])
    platemap_df = pd.read_csv(info["platemap_path"])

    # Step 1: Annotation
    with memray.Tracker(f"{plate}_CFReT_annotate_benchmarks.bin", follow_fork=True):
        annotate(
            profiles=profile_df,
            platemap=platemap_df,
            join_on=["Metadata_well_position", "Image_Metadata_Well"],
            output_file=output_annotated_file,
            output_type="parquet",
        )

    # Load the annotated parquet file to fix metadata columns names
    annotated_df = pd.read_parquet(output_annotated_file)

    # Rename columns using the rename() function
    column_name_mapping = {
        "Image_Metadata_Site": "Metadata_Site",
    }

    annotated_df.rename(columns=column_name_mapping, inplace=True)

    # Save the modified DataFrame back to the same location
    annotated_df.to_parquet(output_annotated_file, index=False)

    # set default for samples to use in normalization
    samples = "all"

    # Only for Plate 4, we want to normalize to the DMSO treatments
    if plate == "localhost231120090001":
        samples = "Metadata_heart_number == 7 and Metadata_treatment == 'DMSO'"

    # Step 2: Normalization
    with memray.Tracker(f"{plate}_CFReT_normalize_benchmarks.bin", follow_fork=True):
        normalized_df = normalize(
            profiles=output_annotated_file,
            method="standardize",
            output_file=output_normalized_file,
            output_type="parquet",
            samples=samples,
        )

    # Step 3: Feature selection
    with memray.Tracker(
        f"{plate}_CFReT_feature_select_benchmarks.bin", follow_fork=True
    ):
        feature_select(
            output_normalized_file,
            operation=feature_select_ops,
            output_file=output_feature_select_file,
            output_type="parquet",
        )
    print(
        f"Annotation, normalization, and feature selection have been performed for {plate}"
    )


# In[5]:


# Check output file
test_df = pd.read_parquet(output_feature_select_file)

print(test_df.shape)
test_df.head(2)
