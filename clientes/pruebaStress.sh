#!/bin/bash
set -e

contador=1
while [ $contador -le 10 ]
do
 python clienteLigero.py 52.176.53.3 luis luis
 (( contador++ ))
done

