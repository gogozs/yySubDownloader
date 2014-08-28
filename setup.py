#!/usr/bin/env python
from setuptools import setup

setup(
    name='yysub',
    version='0.1',
    py_modules=['init'],
    install_requires=['setuptools','lxml'],
    entry_points="""
    [console_scripts]
    yysub = main:main
     """
)
