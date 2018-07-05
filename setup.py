# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

import dblec2018_eval as pkg


cli_name = pkg.__name__.replace('_', '-')
cli_path = f'{pkg.__name__}.scripts:cli'


setup(
    name=pkg.__name__,
    description=pkg.__description__,
    author=pkg.__author__,
    author_email=pkg.__email__,
    version=pkg.__version__,
    pkgs=find_packages(exclude=[]),
    entry_points={
        'console_scripts': [
            f'{cli_name}={cli_path}'
        ]
    },
    install_requires=[
        'click',
        'requests',
        'beautifulsoup4',
        'mecab-python3'
    ],
    dependency_links=[]
)
