#!/bin/bash

export PYTHONPATH=$PYTHONPATH:~/Library/Python/3.7/lib/python/site-packages

rm -rf dist build

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*
