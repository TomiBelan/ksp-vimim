#!/bin/bash

function die {
    echo "$@"
    exit 1
}

if [ $# -ne 3 ]; then
    die "Usage: testovac.sh task_name lang outfile < source_code"
fi
TASKNAME="$1"
LANGUAGE="$2"
exec &>"$3"
#FULLLOG="$4"

if [ "$1" == "" ]; then
    die "Už máš všetky úlohy. Gratulujeme."
fi

cd "`dirname "$0"`"
mkdir -p backup sandbox

if ! [ -f wrapper ]; then
    wrappersrc=wrapper-mj-x86.c
    [ "`uname -m`" == "x86_64" ] && wrappersrc=wrapper-mj-amd64.c
    gcc -O2 -o wrapper $wrappersrc || die "Can't prepare wrapper"
fi

# backup sandbox
tmpdir=backup/`date "+%F-%T"`
mkdir -p "$tmpdir"
cp -r sandbox "$tmpdir" || die "Can't backup"

# clean sandbox
rm -rf sandbox/* || die "Can't clean sandbox"

# copy test data
cp test.sh sandbox/ || die "Can't copy test data"
cp task_data/$TASKNAME/* sandbox/ || die "Can't copy test data"

# compile
cd sandbox || die
cat > "src.$LANGUAGE"
../compile.sh "src.$LANGUAGE" || die "Can't compile file."

MEMORY=25600
TIME=2000
wrapper_args=" -a0 -f -m$MEMORY -t$TIME"
#[ "$FULLLOG" == "true" ] && wrapper_args="--fulllog $wrapper_args"
./test.sh $wrapper_args || die
