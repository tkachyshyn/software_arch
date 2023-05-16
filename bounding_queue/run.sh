#!/bin/bash
python3 producer.py >> result.txt &
python3 consumer.py -n 0 >> result.txt &
python3 consumer.py -n 1 >> result.txt