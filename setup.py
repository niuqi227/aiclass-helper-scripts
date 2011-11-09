#!/usr/bin/env python2

from setuptools import setup

setup(
    name='aiclass-helper-scriptes',
    version='0.0',

    url='https://github.com/bhuztez/aiclass-helper-scripts',
    description='quick and dirty scripts can help you solve some quizzes and homeworks of ai-class',
    
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
    ],

    author='bhuztez',
    author_email='bhuztez@gmail.com',

    requires=['ply'],
    
    packages=['aiclass'],
    test_suite = 'aiclass.tests',
)


