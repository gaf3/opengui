#!/usr/bin/env python

from setuptools import setup

with open("/opt/service/README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="opengui",
    version="0.8.8",
    py_modules = ['opengui'],
    url="https://github.com/gaf3/opengui",
    author="Gaffer Fitch",
    author_email="opengui@gaf3.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
