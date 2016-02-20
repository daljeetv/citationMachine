#!/usr/bin/env python

from setuptools import setup, find_packages
from src import citationmachine
import os


def extra_dependencies():
    import sys
    ret = []
    if sys.version_info < (2, 7):
        ret.append('argparse')
    return ret


def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s
News
====
%(CHANGES)s
""" % read('README', 'CHANGES')

setup(
    name='citationmachine',
    version=citationmachine.__version__,
    description='Instant coding answers via the command line',
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Information Data Mining",
    ],
    keywords='citationmachine helps discover websites from websites you like.',
    author='Daljeet Virdi',
    author_email='daljeetv@gmail.com',
    maintainer='Daljeet Virdi',
    maintainer_email='daljeetv@gmail.com',
    url='https://github.com/dvirdi/Links',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'citationmachine = citationmachine.citationmachine:command_line_runner',
        ]
    },
    install_requires=[
        'pyquery',
        'pygments',
        'requests',
        'requests-cache'
    ] + extra_dependencies(),
)