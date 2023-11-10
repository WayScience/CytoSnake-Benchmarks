from setuptools import find_packages, setup

name = "CytoSnake-Benchmarks"
version = "0.0.1"
description = "Benchmarking for CytoSnake workflows"
url = "https://github.com/WayScience/CytoSnake-Benchmarks"
author = "Erik Serrano"
author_email = "erik.serrano@cuanschutz.com"
license = "BSD-3"


setup(
    name=name,
    version=version,
    description=description,
    long_description="A longer description of your project",
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(),
)
