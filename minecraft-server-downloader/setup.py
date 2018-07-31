import re
import sys
from setuptools import setup, find_packages

setup(
    name='minecraft-server-downloader',
    version='1.0.0',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Simple CLI utility to download vanilla minecraft versions, with help from https://mcversions.net/.',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['download'],
    entry_points = {
        'console_scripts': ['minecraft-server-downloader=download:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "requests-html",
        "requests",
        "click",
        "crayons",
    ]
)