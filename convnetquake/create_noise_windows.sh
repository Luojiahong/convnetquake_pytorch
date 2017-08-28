#!/bin/bash

START=$(date +%s.%N)
N=3

for i in $(seq $N $N 6)
do
    ls data/streams/*29_?-2014* | head -n 6 | head -n $i | tail -n $N | nohup parallel python create_noise_windows.py -c tmp/catalog/Benz.csv -d tmp/train/noises -s {}
done

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

{
    echo To: lijunzhu90@gmail.com
    echo From: gatechzhu@gmail.com
    echo Subject: Work Complete!
    echo
    echo The script create_noise_windows finished in $DIFF seconds
} | ssmtp -vvv lijunzhu90@gmail.com
