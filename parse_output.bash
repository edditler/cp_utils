#!/usr/bin/env bash

for theoutput in "$@"; do
echo $theoutput;
grep 'ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.):' $theoutput | tail -n1;
done
