#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from distutils.command.build import build
from setuptools import setup
from setuptools.command.install import install


# This section drawn from Donald Stufft's article on distributing CFFI
# projects: https://caremad.io/2014/11/distributing-a-cffi-project/
def get_ext_modules():
    import pycohttpparser.backend
    return [pycohttpparser.backend.ffi.verifier.get_extension()]


class CFFIBuild(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)

# Get the version
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open('pycohttpparser/__init__.py', 'r') as f:
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

packages = ['pycohttpparser']

setup(
    name='pycohttpparser',
    version=version,
    description='Python wrapper for picohttpparser',
    long_description=open('README.rst').read() + '\r\n' + open('HISTORY.rst').read(),
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='https://github.com/Lukasa/pycohttpparser',
    packages=packages,
    package_data={'': ['LICENSE', 'README.rst', 'NOTICES']},
    package_dir={'hyper': 'hyper'},
    include_package_data=True,
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
    install_requires=['cffi'],
    setup_requires=['cffi'],
    cmdclass={
        'build': CFFIBuild,
        'install': CFFIInstall,
    },
    zip_safe=False,
)
