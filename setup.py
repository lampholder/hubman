# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='hubman',
    version='0.1',
    description='githubmanager',
    author='Thomas Lant',
    author_email='lampholder@gmail.com',
    url='https://github.com/lampholder/hubman',
    packages=find_packages(exclude=('tests', 'docs'))
)
