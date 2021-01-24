from distutils.core import setup

from setuptools import find_packages

from dcmodule.configs import package_version as _version

_package_name = "dcmodule"
_requires = [
    "pysystem",
]
setup(
    name=_package_name,
    version=_version,
    packages=find_packages(
        include=(_package_name, "%s.*" % _package_name)
    ),
    install_requires=_requires
)
