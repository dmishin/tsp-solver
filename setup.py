#!/usr/bin/env python

from distutils.core import setup

setup(name='tsp_solver',
      version='0.1',
      description='Greedy, supoptimal solver for the Travelling Salesman Problem',
      author='Dmitry Shintyakov',
      author_email='shintyakov@gmail.com',
      url='https://github.com/dmishin/tsp-solver',
      packages=['tsp_solver'],
      scripts=['bin/tsp_demo', 'bin/tsp_numpy2svg']
      )
