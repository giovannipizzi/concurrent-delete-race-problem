#!/bin/bash

python test-conc-delete.py > del.txt &
python test-conc-read.py > read.txt &

wait

# python ../parse-and-plot.py
