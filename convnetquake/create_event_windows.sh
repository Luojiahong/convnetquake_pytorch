#!/bin/bash

START=$(date +%s.%N)

START=$(date +%s.%N)
N = 3

for i in $(seq $N $N 36)
do
    ls data/streams/*029* | head -n $i | tail -n $N | nohup parallel python create_event_windows.py -c tmp/catalog/OK_clustered.csv -d tmp/train/events -s {}
done

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

{
    echo To: lijunzhu90@gmail.com
    echo From: gatechzhu@gmail.com
    echo Subject: Work Complete!
    echo
    echo The script finished in $DIFF seconds
} | ssmtp -vvv lijunzhu90@gmail.com
