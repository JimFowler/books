#! /bin/bash
#
#
#ppxml $1 | egrep -e '(\d+)\s?R[.]?'
ppxml $1 | grep '<Price>' | grep R
