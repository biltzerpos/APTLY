#!/bin/bash

COUNTER=1
output_folder=$1

mkdir $output_folder
while true; do
	echo "FILE NUMBER: $COUNTER"
	rec $output_folder/recording"$COUNTER".wav rate 16k silence 1 0.1 3% 1 3.0 3%
	let COUNTER=COUNTER+1
	
	read -n 1 -t 1 -p "Press Q to quit recording" input
	if [[ $input = "q" ]] || [[ $input = "Q" ]] 
   	then
      		echo # to get a newline after quitting
      		break
   	fi
done
