#!/bin/bash
export PYTHONPATH=src
export SOFTHSM_CONF=tests/softhsm.conf
python -m unittest discover -s tests -p '*.py'

