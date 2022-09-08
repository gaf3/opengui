#!/usr/bin/env python

import os
from setuptools import setup

with open("/opt/service/README.md", "r") as readme_file:
    long_description = readme_file.read()

version = os.environ.get("BUILD_VERSION")

if version is None:
    with open("VERSION", "r") as version_file:
        version = version_file.read().strip()

setup(
    name="opengui",
    version=version,
    py_modules = ['opengui'],
    url=f"https://opengui.readthedocs.io/en/{version}/",
    download_url="https://github.com/gaf3/opengui",
    author="Gaffer Fitch",
    author_email="opengui@gaf3.com",
    description="Library for building dynamic forms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
