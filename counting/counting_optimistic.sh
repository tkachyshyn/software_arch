#!/bin/bash

python3 counting_optimistic.py -n 0 >> optimistic_results.txt &
python3 counting_optimistic.py -n 1 >> optimistic_results.txt &
python3 counting_optimistic.py -n 2 >> optimistic_results.txt
