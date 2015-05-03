#!/bin/bash

export PYTHONPATH=.:tests

for i in tests/*.py
do
    $i
done

