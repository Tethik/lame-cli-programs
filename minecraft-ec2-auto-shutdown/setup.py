import re
import sys
from setuptools import setup, find_packages

setup(
    name='minecraft-ec2-auto-shutdown',
    version='1.0.0',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Linux service to monitor and automatically shut down a Minecraft EC2 instance',
    url='https://github.com/Tethik/lame-cli-programs',
    py_modules=['minecraft_server_downloader'],
    entry_points = {
        'console_scripts': ['minecraft-ec2-auto-shutdown=minecraft_ec2_auto_shutdown:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[
        "boto3",
        "appdirs",
        "ec2-metadata",
        "mcipc @ https://github.com/conqp/mcipc#egg=mcipc",
    ]
)