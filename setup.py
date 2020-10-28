import os
from codecs import open
from distutils.core import setup

from setuptools import find_packages
from dcmodule.configs.version import version

_package_name="dcmodule"

setup(
    python_requires=">=3.5",
    install_requires=[
        'where>=1',
        'pytz>=2018',
        'tzlocal>=2',
        'click>=7',
        'colorama>=0.4',
        'prettytable>=1',
    ],
    tests_require=[
        'pytest>=3',
        'pytest-cov',
        'pytest-mock',
    ],
    include_package_data=True
)
