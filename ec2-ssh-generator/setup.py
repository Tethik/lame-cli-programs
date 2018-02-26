import re
import sys
from setuptools import setup, find_packages

setup(
    name='ec2sshgen',
    version='0.0.1',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Generates Host stanzas for your ssh config for your AWS EC2 instances based on a "Domain" tag.',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['ec2sshgen'],
    entry_points = {
        'console_scripts': ['ec2sshgen=ec2sshgen:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "boto3",
    ]
)