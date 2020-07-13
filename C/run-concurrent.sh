#!/bin/bash

make || exit 1

#if [ ! -d trash ] 
#then
#    mkdir trash
#fi

FAIL=0

./conc-delete > del.txt &
./conc-read > read.txt &

for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done

exit $FAIL

#python ../parse-and-plot.py
