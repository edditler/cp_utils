#!/usr/bin/env bash

lengths=$(grep -P "^\s+\d+" $1 | uniq)
nl=$(echo $lengths | wc -w);

if [[ $nl -eq 1 ]]; then
  cat $1 > ${1}_cleaned.xyz;
elif [[ $nl -eq 2 ]]; then
  for l in $lengths; do
    n=$(grep -P -n "^[^=]    $l" $1 | tail -n1 | cut -f1 -d:)
    echo "writing ${1}_cleaned.xyz";
    tail -n +$(echo "$n+$l+2" | bc -l) $1 > ${1}_cleaned.xyz;
    break;
  done
else
  echo "PANIC! There is more than two results for natoms!"
fi
