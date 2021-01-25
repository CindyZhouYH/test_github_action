import os
import sys
from distutils.core import setup

from setuptools import find_packages

from codecs import open

_package_name = "dcmodule"
here = os.path.abspath(os.path.dirname(__file__))
meta = {}
with open(os.path.join(here, _package_name, 'configs', 'meta.py'), 'r', 'utf-8') as f:
    exec(f.read(), meta)

_package_version = meta['__VERSION__']
_package_name = meta['__TITLE__']

setup(
    name=_package_name,
    version=_package_version,
    packages=find_packages(
        include=(_package_name, "%s.*" % _package_name)
    ),
    author=meta['__AUTHOR__'],
    author_email=meta['__AUTHOR_EMAIL__'],
    python_requires=">=3.5",
    install_requires=[
        'click>=7',
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

sys.stderr.write("without switch user function")
