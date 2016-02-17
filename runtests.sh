#!/bin/bash
set -xe
export PYTHONPATH=src
python -m unittest discover -s tests -p '*.py'
wget -S --no-check-certificate --post-file=tests/query.data --header "Content-type: application/x-www-form-urlencoded" https://localhost:8890/anchor -O tmp/reply
diff -bu testserver/expectedreply tmp/reply 

