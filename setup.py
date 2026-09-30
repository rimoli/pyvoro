#
# setup.py : pyvoro python interface to voro++
#
# this extension to voro++ is released under the original modified BSD license
# and constitutes an Extension to the original project.
#
# Copyright (c) Joe Jordan 2012
# contact: <joe.jordan@imperial.ac.uk> or <tehwalrus@h2j9k.org>
#
# The package metadata is in pyproject.toml; this file only describes the
# extension module. The Cython wrapper is compiled at build time, so that
# the generated C++ code always matches the Python version it is built for.
#

from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension("pyvoro.voroplusplus",
              sources=["pyvoro/voroplusplus.pyx",
                       "pyvoro/vpp.cpp",
                       "src/voro++.cc"],
              include_dirs=["src"],
              language="c++",
              )
]

setup(ext_modules=cythonize(extensions,
                            compiler_directives={"language_level": 3}))
