#!/bin/bash
set -xe
export PYTHONPATH=src:tests:cryptoserver
export SOFTHSM_CONF=tests/softhsm.conf
/usr/bin/python3 -m unittest discover -s tests -p '*.py'
/usr/bin/python3 -m unittest discover -s integrationtests -p '*.py'
wget -S --no-check-certificate --post-file=tests/query.data --header "Content-type: application/x-www-form-urlencoded" https://localhost:8890/anchor -O tmp/reply
diff -bu testserver/expectedreply tmp/reply 

