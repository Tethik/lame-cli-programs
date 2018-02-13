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
    py_modules=['vaultauth'],
    entry_points = {
        'console_scripts': ['vaultauthpy=vaultauth:main'],
    },
    scripts = ['bin/vaultauth'],
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "hvac",
        "keyring",
        "keyrings.alt"
    ]
)