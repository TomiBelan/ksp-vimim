#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: compile.sh filename"
    exit 1
fi

filename="$1"
if [ "${filename: -4}" == ".cpp" ]; then
    g++ -static -W -Wall $filename -o program || exit 1
elif [ "${filename: -4}" == ".pas" ]; then
    fpc  $filename -oprogram || exit 1
else
    echo "Unknown extension";
    exit 1;
fi
