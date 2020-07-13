#!/bin/bash

make || exit 1

#if [ ! -d trash ] 
#then
#    mkdir trash
#fi

./conc-delete > del.txt &
./conc-read > read.txt &

wait

#python ../parse-and-plot.py
