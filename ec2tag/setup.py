import re
import sys
from setuptools import setup, find_packages

setup(
    name='ec2-by-tag',
    version='0.0.1',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Program to fetch ec2 instance private ips by their "Name" tag',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['vaultauth'],
    entry_points = {
        'console_scripts': ['ec2-by-tag=ec2tag:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "boto3",
    ]
)