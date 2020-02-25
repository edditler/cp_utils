#!/usr/bin/env bash

for theoutput in "$@"; do
  echo $theoutput;
  grep 'ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.):' $theoutput | tail -n1;
  
  script_folder=$(dirname $0)
  # -n: no new line
  # -e: escape strings
  echo -ne '\033[0;31m'; # red
  bash $script_folder/is_converged.bash $theoutput;
  echo -ne '\033[0m'; # no color
done
