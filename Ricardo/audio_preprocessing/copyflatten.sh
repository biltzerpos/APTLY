#!/bin/bash


# This script is used to copy all the bmp files from a folder (and subfolders) into an output directory.

i=1
random=file
output_folder=$2
mkdir $output_folder

#Change below to get only the file types you're interested
find $1 -name "*.wav" -type f | while read f
do
	newbase=${f/*./$random$i.}
	cp $f ./$output_folder/"$newbase"
	((i++))
done
