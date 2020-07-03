#!/usr/bin/env bash

for theoutput in "$@"; do
    if grep -q 'exceeded requested execution time' $theoutput; then
        echo "$theoutput exceeded requested execution time";
    fi
    if grep -q 'MAXIMUM NUMBER OF OPTIMIZATION STEPS REACHED' $theoutput; then
        echo "$theoutput exceeded number of optimization steps";
    fi
done
