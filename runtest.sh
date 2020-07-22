#!/bin/sh
PYTHONPATH=$PYTHONPATH:tests python -m unittest "$1"
