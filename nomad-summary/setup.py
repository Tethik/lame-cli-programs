import re
import sys
from setuptools import setup, find_packages

setup(
    name='nomad-summary',
    version='1.0.0',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Calculates and displayes summary of total memory and CPU requirements set on your currently running Nomad jobs.',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['nomad_summary'],
    entry_points={
        'console_scripts': ['nomad-summary=nomad_summary:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "python-nomad",
        "click",
        "terminaltables",
    ]
)
