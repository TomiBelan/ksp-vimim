#!/bin/bash
echo "Testing task..."

echo "Using parameters: $*"
SHOW_DIFF=0
if [ "$1" == "--fulllog" ]; then
    SHOW_DIFF=1
    shift
fi

for infile in *.in; do
    echo "********* Testing $infile ********"

    base=${infile%.in}
    outfile=$base.out
    tstfile=$base.tst
    difffile=$base.diff
    echo -n "running..."
    ../wrapper "$@" ./program -i$infile -o$outfile &>tmp
    RETVAL=$?
    cat tmp

    if grep EXC tmp; then
        echo "RUNTIME EXCEPTION"
    fi

    if grep TLE tmp; then
        echo "TIME LIMIT EXCEEDED"
    fi

    if grep SEC tmp; then
        echo "SECURITY EXCEPTION"
    fi

    if [ "$RETVAL" -ne 0 ]; then
        echo "FAILED (retval $RETVAL)"
        exit 1
    fi

    diff -u $outfile $tstfile > $difffile
    DIFFRES=$?

    if [ $SHOW_DIFF -ne 0 ]; then
        echo "[begin diff]"
        cat $difffile
        echo "[end diff]"
    fi

    if [ "$DIFFRES" -ne 0 ]; then
        echo "WRONG ANSWER"
        exit 1
    fi
    echo "OK"
done
echo
echo "EVERYTHING OK"
exit 0
