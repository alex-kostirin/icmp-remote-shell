#!/usr/bin/env python

from distutils.core import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='icmp-remote-shell',
      version='1.0',
      description='Prototype of steganography remote shell using ICMP protocol for data hiding',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alexey Kostyrin',
      author_email='alex.kostirin@ya.ru',
      url='https://gitlab.com/alex-kostirin/icmp-remote-shell',
      packages=setuptools.find_packages(),
      entry_points={
          'console_scripts': ['icmp-remote-shell-client=icmp_remote_shell.client:main',
                              'icmp-remote-shell-server=icmp_remote_shell.server:main'],
      },
      classifiers=(
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ),

      )
