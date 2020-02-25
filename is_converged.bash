#!/usr/bin/env bash

for theoutput in "$@"; do
    if grep -q 'exceeded requested execution time' $theoutput; then
        echo "$theoutput exceeded requested execution time";
    fi
done
