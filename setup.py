import os
from distutils.core import setup

from setuptools import find_packages

from codecs import open

_package_name = 'dcmodule'
here = os.path.abspath(os.path.dirname(__file__))
meta = {}
with open(os.path.join(here, _package_name, 'configs', 'version.py'), 'r', 'utf-8') as f:
    exec(f.read(), meta)

_version = meta['version']

setup(
    name=_package_name,
    version=_version,
    packages=find_packages(
        include=(_package_name, "%s.*" % _package_name)
    ),
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
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dcmodule=dcmodule.entrance.cli:cli'
        ]
    },

)
