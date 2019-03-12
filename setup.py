#!/usr/bin/env python
import re
from os.path import dirname, join

from setuptools import setup


def read_version(path):
    with open(path) as f:
        text = f.read()
        version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', text, re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='devsecrets',
    version=read_version(join(dirname(__file__), 'src', 'devsecrets', 'version.py')),
    description="Read secrets from environment variables or files",
    keywords="secret secrets password passwords".split(),
    packages=['devsecrets'],
    package_dir={'devsecrets': 'src/devsecrets'},
    install_requires=[
        'toml'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
