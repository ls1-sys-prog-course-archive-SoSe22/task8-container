#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "USAGE: $0 task-name" >&2
fi

taskname=$1

sed -i -e "s!task-name!${taskname}!g" Makefile Cargo.toml
mv task-name.cpp "${taskname}.cpp"
mv task-name.c "${taskname}.c"
rm "$0"
git add task-name.cpp "${taskname}.cpp" task-name.c "${taskname}.c" "$0" Cargo.toml Makefile
