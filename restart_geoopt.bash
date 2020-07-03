#!/usr/bin/env bash

backto=$PWD;
echo $backto;

for theoutput in "$@"; do
    if grep -q 'GEO run terminated' $theoutput; then
        echo $calc;
        cd $(dirname $theoutput);
        cp -v inp old_inp;
        mv -v out old_out;
        mv -v zirc-1.restart inp;
        cp -v ~/run*.bash .
        sbatch run*.bash;
        cd $backto;
    fi
done
