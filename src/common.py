"""
Module: common.py

Description:
The `common.py` module contains essential I/O and file manipulation utilities
for streamlined code reusability and maintainability within the project. These
utilities include functions for reading, writing, copying, moving, and managing
files, as well as handling directories. Importing this module simplifies and
standardizes common I/O tasks across the project, promoting efficiency and
organization.
"""

import pathlib
from collections import defaultdict
from typing import Optional


def validate_path(
    path: str | pathlib.Path, check_dir: Optional[bool] = False
) -> pathlib.Path:
    """Checks path if it is valid. If the path is a str type, it will return a
    pathlib.Path object

    Parameters
    ----------
    path : str | pathlib.Path
        path to file

    is_dir: Optional[bool]
        additional check to ensure that the path provided is a directory

    Returns
    -------
    pathlib.Path
        valid path

    Raises
    ------
    TypeError
        Raised if incorrect types passed into the function
    FileNotFoundError
        Raised if provided path is not found
    """

    # type checking
    if not isinstance(path, (str, pathlib.Path)):
        raise TypeError(
            "'path' must be a str or a pathlib.Path object. " f"Provided: {type(path)}"
        )

    # if the path is str type, convert to pathlib.Path
    # raise error if path is not valid
    if isinstance(path, str):
        path = pathlib.Path(path).resolve(strict=True)

    # if a pathlib.Path object has been provided, check if the path exists
    if isinstance(path, pathlib.Path) and not path.exists():
        raise FileNotFoundError(f"Path {str(path)} is not found")

    # additional check to ensure if it is a directory
    if check_dir and not path.is_dir():
        raise TypeError("`path` is not a directory")

    return path


def get_benchmark_files(
    benchmark_path: str | pathlib.Path, ext: str
) -> list[pathlib.Path]:
    """Gets files from the `benchmarks` based on provided extensions: '.bin' or '.json'

    Parameters
    ----------
    benchmark_path : str | pathlib.Path
        path to benchmark directory

    Returns
    -------
    list[pathlib.Path]
        list of all json file paths
    """

    # validating path
    benchmark_path = validate_path(benchmark_path)

    # cleaning up extension
    ext = ext.replace(".", "").strip()
    if ext not in ["bin", "json"]:
        raise ValueError(f"'{ext}' is not a supported extension")

    # select benchmark files
    bench_files = list(benchmark_path.glob(f"*.{ext}"))
    if len(bench_files) == 0:
        raise ValueError("Unable to find `json` files inside the benchmarks folder")

    return bench_files


# TODO: work in progress
def report_plots_to_readme(readme_path: str | pathlib.Path) -> None:
    """Adds performance report into the benchmark readme

    Parameters
    ----------
    readme_path : str | pathlib.Path
        _description_
    """

    readme_path = validate_path(readme_path)
    # check if "## generated plots exists within the read me"
    # if so, skip
    with open(readme_path, mode="r", encoding="utf-8") as contents:
        md_lines = contents.readlines()

    if not any(line.strip() == "## generated plots" for line in md_lines):
        # grab paths of generated plots and convert into dict

        ## append new contents to md file
        with open(readme_path, mode="a", encoding="utf-8") as stream:
            # create a docstring that will be added into the readme
            report = """
            add new contents here


            """

            # append to md file
            stream.write(report)

    # if the content already exists, there's no need to run this.
    print("Warning: plot already exists in the MD file. Skipping...")


def create_filename_path_mapping(
    fnames: str | list[str], data_dir: str | pathlib.Path, data_ext: str
) -> dict:
    """Generates a mapping that associates the file's basename with its respective
    location of the data file.  This is accomplished by specifying the directory
    path where the data is stored. This functionality also extends to symbolic
    links.

    Parameters
    ----------
    fnames : str | list[str] or list of str
        A single filename or a list of filenames (strings) or symbolic links.

    data_dir : str | pathlib.Path
        A string representing the directory path where the data files are located,
        or a pathlib.Path object.

    data_ext : str
        The file extension (without a dot) of the data files to be considered
        when creating the mapping.

    Returns
    -------
    dict
        A dictionary where keys are filenames or symbolic link names and values
        are the corresponding paths to the data files.
    """

    # convert to list if only a string is passed
    if isinstance(fnames, str):
        fnames = [str]

    # check path
    data_dir = validate_path(data_dir, check_dir=True)
    data_ext = data_ext.strip().replace(".", "")

    # collect all data files
    labeled_inputs = defaultdict(lambda: None)
    for data_file in data_dir.glob(f"*.{data_ext}"):
        for fname in fnames:
            if data_file.name.startswith(fname):
                labeled_inputs[fname] = str(data_file)
    return labeled_inputs
