# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

import dblec2018_eval as pkg


setup(
    name=pkg.__name__,
    description=pkg.__description__,
    author=pkg.__author__,
    author_email=pkg.__email__,
    version=pkg.__version__,
    pkgs=find_packages(exclude=[]),
    install_requires=[],
    dependency_links=[]
)
