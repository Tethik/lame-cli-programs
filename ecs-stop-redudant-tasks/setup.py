import re
import sys
from setuptools import setup, find_packages

setup(
    name='ecs-stop-redundant-tasks',
    version='0.0.1',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Finds and stops old ecs tasks if there is a newer version available (based on docker tag).',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['ecs_stop_redundant_tasks'],
    entry_points = {
        'console_scripts': ['ecs_stop_redundant_tasks=ecs_stop_redundant_tasks:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "boto3",
        "crayons",
    ]
)