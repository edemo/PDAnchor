#!/bin/bash

export PYTHONPATH=.:tests

for i in tests/*.test
do
    $i
done

