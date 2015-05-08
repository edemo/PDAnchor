#!/bin/bash
PYTHONPATH=src:test python -m unittest discover -s tests -p '*.py'

