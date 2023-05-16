#!/bin/bash

python3 counting_no_lock.py -n 0 >> no_lock_results.txt &
python3 counting_no_lock.py -n 1 >> no_lock_results.txt &
python3 counting_no_lock.py -n 2 >> no_lock_results.txt
