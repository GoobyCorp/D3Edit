#!/usr/bin/env bash

curdir=$(echo "${0}" | awk -F '/' 'BEGIN {OFS = FS}/\//{$NF="";print}')
cd "${curdir}"
. ./venv/bin/activate
python D3Edit.py