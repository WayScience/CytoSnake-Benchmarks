"""
This script is designed to parse benchmark outputs and generate informative
plots and figures that help evaluate the performance of various workflows.
"""


def parse_memray_outputs():
    """Wrapper function that spawns subprocess that calls `memray` cli commands to parse
    all the outputs.

    The outputs generated from this wrapper are:
    - json files (JSON) format
    - flamgraphs (HTML) format
    - tables (HTML) format
    -


    Returns
    -------
    None
        Generates outputs files that contains all the information of each benchmark
    """
