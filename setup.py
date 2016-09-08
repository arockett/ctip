# -*- coding: utf-8 -*-
"""
Setup script for ctip.

Created on Sat Jul  9 16:58:24 2016

@author: Aaron Beckett
"""

import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('ctip/entrypoint.py').read(),
    re.M
).group(1)
    

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
    
    
setup(
    name = "ctip",
    version = version,
    author = "Aaron Beckett",
    author_email = "aminor65ii@gmail.com",
    description = "Extendible configuration testing in parallel.",
    long_description = long_descr,
    license = "MIT",
    url = "https://github.com/becketta/ctip.git",
    packages = ["ctip"],
    install_requires = [
        'pyparsing'
    ],
    entry_points = {
        "console_scripts": ['ctip = ctip.entrypoint:main']
    },
    platforms = ["any"],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities"
    ],
    keywords = "config configuration test testing parallel research tool optimization"
)