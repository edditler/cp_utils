#!/usr/bin/env bash

if [ $# -eq 1 ]; then
    coords=$1
    slabatom="Zr"
else
    coords=$1
    slabatom=$2
fi

n=$(grep -n "${slabatom}" $coords | head -n1 | awk '{print $1}' | tr -d ':')
nn=$(echo "$n-1" | bc)
nn2=$(echo "$nn-2" | bc)

echo $nn2;
echo "";
head -n $nn $coords | tail -n $nn2;
