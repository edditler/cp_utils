#!/usr/bin/env bash

# "Parse" cli arguments
if [[ $# -eq 0 ]] ; then
    echo "You have to provide the folder to restart."
    exit 1
fi

dir=${1%/}
echo "=== === === === === ==="
echo "Taking the calculation in ${dir}..."

# What do we need?
files_to_save=("out"
                "*-pos-1.xyz"
                "*-RESTART.wfn"
                "*-1.restart"
                "run*.bash"
                "coords.xyz")

# Determine the new name of the folder
newdir="${dir%/}_re"

# Action!
mkdir $newdir
for fts in "${files_to_save[@]}"; do
    cp -v ${dir}/${fts} ${newdir}
done

mv -v ${newdir}/*-1.restart ${newdir}/inp

# And move the old folder into the new one!
mv -v $dir/ $newdir/
