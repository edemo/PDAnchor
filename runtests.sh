#!/bin/bash
set -e
export PYTHONPATH=src:tests:cryptoserver
/usr/bin/python3 -m unittest discover -s tests -p '*.py'
/usr/bin/python3 -m unittest discover -s integrationtests -p '*.py'

tools/e2e
