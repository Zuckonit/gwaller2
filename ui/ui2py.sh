#!/bin/bash

CMD=/usr/bin/pyuic4
APPNAME=`basename $0`

function usage{
    echo "
            ----------------------------
            +         $APPNAME         +
            +           _by Yang yiming+
            ----------------------------
    convert the ui file to py file in current directory
        >>$APPNAME file1.ui [file2.ui ...]
        >>$APPNAME pattern

    example:
        >>$APPNAME login.ui
        >>$APPNAME *.ui "
}

function convert{
    for f in $@; do
        bname=`basename $f`
        name=${bname%.*}
        echo $f | egrep "*.ui$" && $CMD $f > $name.py
    done
}

[ $# -lt 1 ] && usage && exit 1

convert $@
exit 0
