#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup and distribution."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2020 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

import os
from os import path
from setuptools import find_packages, setup
import sys

from stackmud import __author__, __contact__, __homepage__, get_version


PROJECT_ROOT = path.dirname(path.abspath(__file__))


with open(path.join(PROJECT_ROOT, "README.md")) as readme:
    long_description = readme.read()


setup(
    name="stackmud",
    version=get_version(),
    # PyPI metadata
    description="StackMUD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__contact__,
    url=__homepage__,
    license="MIT",
    keywords=["stackmud", "mud", "mux", "moo", "mush"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # Packaging
    packages=find_packages(),
    zip_safe=False,
    # Requirements
    install_requires=[],
)
