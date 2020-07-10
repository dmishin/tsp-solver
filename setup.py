#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='tsp_solver2',
      version='0.4',
      description='Greedy, suboptimal solver for the Travelling Salesman Problem',
      author='Dmitry Shintyakov',
      author_email='shintyakov@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/dmishin/tsp-solver',
      packages=['tsp_solver', 'tsp_solver.demo'],
      keywords=['travelling salesman problem', 'optimization'],
      scripts=['bin/tsp_demo', 'bin/tsp_numpy2svg'],
      license="free domain",
      classifiers=[
          'License :: Public Domain',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      )
