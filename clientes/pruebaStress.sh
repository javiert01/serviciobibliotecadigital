#!/bin/bash
set -e

contador=1
while [ $contador -le 1000 ]
do
 python clienteLigero.py 192.168.1.3
 (( contador++ ))
done

