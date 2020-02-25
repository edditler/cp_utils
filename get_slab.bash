#!/usr/bin/env bash

if [ $# -eq 1 ]; then
    coords=$1
    slabatom="Zr"
else
    coords=$1
    slabatom=$2
fi

tot=$(wc -l $coords | awk '{print $1}')
n=$(grep -n "$slabatom" $coords | head -n1 | tr ':' ' ' | awk '{print $1}')

nn=$(echo "$tot-$n+1" | bc)

echo $nn
echo ""
tail -n $nn $coords
