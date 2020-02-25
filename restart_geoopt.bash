#!/usr/bin/env bash

backto=$PWD;
echo $backto;

for theoutput in "$@"; do
    if grep -q 'GEO run terminated' $theoutput; then
        echo $calc;
        cd $(dirname $calc);
        cp -v inp old_inp;
        mv -v zirc-1.restart inp;
        sbatch run*.bash;
        cd $backto;
    fi
done
