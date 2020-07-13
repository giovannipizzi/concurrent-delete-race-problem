#!/bin/bash

FAIL=0

python test-conc-delete.py > del.txt &
python test-conc-read.py > read.txt &


for job in `jobs -p`
do
echo $job
    wait $job || let "FAIL+=1"
done

exit $FAIL

# python ../parse-and-plot.py
