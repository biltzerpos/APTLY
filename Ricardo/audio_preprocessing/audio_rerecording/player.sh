#!/bin/bash

dirpath=$1
delay=$2
count=1

for filename in "$dirpath"/*.wav; do
	echo ">>>Playing audio number $count : $filename"
	play "$filename"
	sleep "$delay"
	count=$(($count + 1))
done
