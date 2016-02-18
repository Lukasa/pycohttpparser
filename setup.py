#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import setup, find_packages


# Get the version
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open('src/pycohttpparser/__init__.py', 'r') as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        version = match.group(1)
    else:
        raise RuntimeError("No version number found!")

# Stealing this from Kenneth Reitz
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pycohttpparser',
    version=version,
    description='Python wrapper for picohttpparser',
    long_description=open('README.rst').read() + '\r\n' + open('HISTORY.rst').read(),
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='https://github.com/Lukasa/pycohttpparser',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['cffi>=1.0.0'],
    setup_requires=['cffi>=1.0.0'],
    zip_safe=False,
    cffi_modules=["src/pycohttpparser/build.py:ffi"],
    ext_package="pycohttpparser",
)
