#!/bin/sh
# 07/11/2018
# This code is used to apply a highpass filter to the audio tracks to a given value.
# It needs 3 arguments as input. First argument is input directory which contain wav files.
# Second argument is output directory that you want to create to store upsampled/downsampled files.Third argument is 
# the value of the frequency you will use for a highpass filter.
# The input directory can have wav files or subfolders or both. For all the wav files it creates one text 
# file.
# For all the subfolders, it creates separate text files for each folder.
# Created by: Ricardo Reimao based on scripts from Prof. Vassilios Tzerpos
#


indir="$1"
outdir="$2"
rateValue="$3"

if test $# -ne 3
        then
        echo "%highpassfilter"
	echo "Usage: highpassfilter.sh <indir> <outdir> <frequency>"
        echo "Enter name of input directory as first argument, input directory should already exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist before"
	echo "Enter the value to which you want to apply the highpass filter to the tracks as third argument"
        exit 0
fi            


if test ! -d "$indir"
then
echo "Input directory does not exist"
exit 0
fi


if test -d "$outdir"
then
echo "Output directory already exist, Please give another name for output directory"
exit 0
fi


if [[ -z "$rateValue" || $rateValue == *[^[:digit:]]* ]]; then
echo Please enter a valid number for highpass frequency. 
exit 0
fi 

mkdir "$outdir"

for dir in "$indir"/*
do
	subDir=$(basename $dir)
	if test -f "$dir" # if it is file then create converted file directly in output directory
	then
       		sox "${dir%/}" "$outdir"/"${subDir%.wav}".wav highpass $rateValue
      	fi

	if test -d "$dir" # if it is directory i.e. sub directory, then create a new directory in output 
	# directory with same name as input sub directory. And store converted files in new output sub 
	# directory.
	then
		mkdir "$outdir"/"$subDir"
		for track in "$dir"/*.wav
		do
			file=$(basename "$track")
			sox "$track" "$outdir"/"$subDir"/"${file%.wav}".wav highpass $rateValue
		done
	fi
done
