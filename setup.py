#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='tsp_solver2',
      version='0.3',
      description='Greedy, suboptimal solver for the Travelling Salesman Problem',
      author='Dmitry Shintyakov',
      author_email='shintyakov@gmail.com',
      url='https://github.com/dmishin/tsp-solver',
      packages=['tsp_solver', 'tsp_solver.demo'],
      keywords=['travelling salesman problem', 'optimization'],
      scripts=['bin/tsp_demo', 'bin/tsp_numpy2svg'],
      license="free domain"
      )
