#!/usr/bin/env python

from setuptools import setup
setup(
    name="opengui",
    version="0.8.7",
    py_modules = ['opengui'],
    url="https://github.com/gaf3/opengui",
    author="Gaffer Fitch",
    author_email="opengui@gaf3.com",
    long_description="Library for building dynamic forms, forms whose options and even fields change based on values in other fields.",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
