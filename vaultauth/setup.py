import re
import sys
from setuptools import setup, find_packages

setup(
    name='vaultauth',
    version='0.0.1',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Program to authenticate into vault',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['auth'],
    entry_points = {
        'console_scripts': ['vaultauth=auth:main'],
    },
    zip_safe=True,
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "hvac"
    ]
)