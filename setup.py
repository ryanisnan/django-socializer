#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-socializer',
    version='0.0.1',
    description='A generic set of utilities for making django models social.',
    author='Ryan West',
    author_email='ryanisnan@gmail.com',
    url='http://github.com/ryanisnan/django-socializer/',
    packages=['socializer'],
    zip_safe=False,
    requires=[],
    install_requires=[],
    classifiers=[],
)