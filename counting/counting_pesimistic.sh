#!/bin/bash

python3 counting_pesimistic.py -n 0 >> pesimistic_results.txt &
python3 counting_pesimistic.py -n 1 >> pesimistic_results.txt &
python3 counting_pesimistic.py -n 2 >> pesimistic_results.txt
