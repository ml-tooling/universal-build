#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created based on: https://github.com/kennethreitz/setup.py/blob/master/setup.py
# Alternative: https://github.com/seanfisk/python-project-template/blob/master/setup.py.tpl
# https://github.com/pypa/sampleproject/blob/master/setup.py
# https://blog.ionelmc.ro/2014/05/25/python-packaging

from __future__ import absolute_import, print_function

import io
import os
import sys
from glob import glob
from os.path import basename, splitext

from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = "universal-build"
MAIN_PACKAGE = "universal_build"  # Change if main package != NAME
DESCRIPTION = "Universal build utilities for all ml-tooling components."
URL = "https://github.com/mltooling/universal-build"
EMAIL = "team@mltooling.org"
AUTHOR = "ML Tooling Team"
LICENSE = "MIT"
REQUIRES_PYTHON = ">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*"
VERSION = (
    None  # Only set version if you like to overwrite the version in __version__.py
)

# Please define the requirements within the requirements.txt

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

# Check if version is right
if sys.version_info[:2] < (2, 7) or (
    sys.version_info[:1] == 3 and sys.version_info[:2] < (3, 5)
):
    raise Exception("This package needs Python 2.7 or 3.5 or later.")  # Python 2.7,

PWD = os.path.abspath(os.path.dirname(__file__))


def load_requirements(path_dir=PWD, file_name="requirements.txt", comment_char="#"):
    """Read requirements file and return packages and git repos separately."""
    requirements = []
    dependency_links = []
    with open(os.path.join(path_dir, file_name), "r", encoding="utf-8") as file:
        lines = [ln.strip() for ln in file.readlines()]
    for ln in lines:
        if not ln:
            continue
        if comment_char in ln:
            ln = ln[: ln.index(comment_char)].strip()
        if ln.startswith("git+"):
            dependency_links.append(ln.replace("git+", ""))
        else:
            requirements.append(ln)
    return requirements, dependency_links


# Read the requirements.txt and use it for the setup.py requirements
requirements, dependency_links = load_requirements()
if dependency_links:
    print(
        "Cannot install some dependencies. "
        "Dependency links are currently not supported: " + str(dependency_links)
    )
dev_requirements, _ = load_requirements(file_name="requirements-dev.txt")

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(PWD, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}  # type: dict
if not VERSION:
    with open(os.path.join(PWD, os.path.join("src", MAIN_PACKAGE), "about.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

# where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description="%s\n\nRequirements:\n%s" % (long_description, requirements),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license=LICENSE,
    packages=find_packages(where="src", exclude=("tests", "test")),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        # TODO: update this list to match your application: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # 'Programming Language :: Python :: 3 :: Only',
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={
        # If tPWD are data files included in your packages that need to be
        # 'sample': ['package_data.dat'],
    },
    project_urls={
        "Changelog": URL + "/blob/main/CHANGELOG.md",
        "Issue Tracker": URL + "/issues",
        "Source": URL,
    },
    entry_points={
        # 'console_scripts': ['cli-command=my_package.cli_handler:cli'],
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    extras_require={
        # extras can be installed via: pip install package[dev]
        "dev": [dev_requirements],
    },
    setup_requires=[],
)
