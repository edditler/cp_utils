#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    coordfile="zirc-pos-1.xyz"
else
    coordfile=$1
fi

if [[ ! -f $coordfile ]]; then
    >&2 echo "The file ${coordfile} doesn't exist!"
    exit 1
fi

natoms=$(head -n1 $coordfile | tr -d '[:space:])
nlines=$(echo "$natoms+2" | bc -l)
tail -n $nlines $coordfile
