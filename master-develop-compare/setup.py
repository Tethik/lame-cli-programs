import re
import sys
from setuptools import setup, find_packages

setup(
    name='master-develop-compare',
    version='1.0.0',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Tool to compare repository master and develop branches for changes using the github api in bulk.',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['master_develop_compare'],
    entry_points = {
        'console_scripts': ['master-develop-compare=master_develop_compare:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "requests",
        "click",
        "crayons",
        "keyring",
    ]
)