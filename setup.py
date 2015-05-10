#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='python-stubhub',
      version='0.1a',
      description='A library to simplify the use of the StubHub API.',
      url='http://github.com/jmickela/python-stubhub',
      install_requires=["requests"],
      author='Jason Mickela',
      author_email='jason@rootid.in',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)