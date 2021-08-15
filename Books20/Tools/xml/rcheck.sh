#! /bin/bash
#
#
ppxml $1 | egrep -e '[1-9]+R' | grep -v Price
