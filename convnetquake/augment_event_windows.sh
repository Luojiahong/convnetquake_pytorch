#!/bin/bash

START=$(date +%s.%N)

SRC_DIR="tmp/train/events"
DST_DIR="tmp/train/augmented_events"
TOTAL=$(ls ${SRC_DIR} | wc -l)
N=$(getconf _NPROCESSORS_ONLN)

for i in $(seq ${N} ${N} ${TOTAL})
do
    ls ${SRC_DIR} | head -n ${i} | tail -n $N | nohup parallel python augment_event_windows.py  -d ${DST_DIR} -s {}
done

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

{
    echo To: lijunzhu90@gmail.com
    echo From: gatechzhu@gmail.com
    echo Subject: Work Complete!
    echo
    echo The script augment_event_windows finished in ${DIFF} seconds
} | ssmtp -vvv lijunzhu90@gmail.com