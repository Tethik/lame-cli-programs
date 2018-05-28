import re
import sys
from setuptools import setup, find_packages

setup(
    name='docker-branch-tagging',
    version='0.0.1',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Utility tool to help you give your docker images multiple tags based on the current git branch.',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['ecs_stop_redundant_tasks'],
    entry_points = {
        'console_scripts': ['docker-branch-tagging=docker_branch_tagging:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "click",
    ]
)