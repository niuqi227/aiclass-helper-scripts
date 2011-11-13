#!/usr/bin/env python2

from setuptools import setup

setup(
    name='aiclass-helper-scripts',
    version='0.1',

    url='https://github.com/bhuztez/aiclass-helper-scripts',
    description='quick and dirty scripts can help you solve some quizzes and homeworks of ai-class',
    
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
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

    entry_points = {
        'console_scripts': [
            'aiclass = aiclass.__main__:main',
        ]
    },

)


