#!/bin/sh
# 20/09/2018
# This code is used to downsample/upsample the audio tracks to the given value.
# It needs 3 arguments as input. First argument is input directory which contain wav files.
# Second argument is output directory that you want to create to store upsampled/downsampled files.Third argument is 
# the value of sample rate that you want to convert
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
        echo "%changesamplerate"
	echo "Usage: changesamplerate.sh <indir> <outdir> <sampleratevalue>"
        echo "Enter name of input directory as first argument, input directory should already exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist before"
	echo "Enter the value to which you want to updasample/downsample the tracks as third argument"
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
echo Please enter a valid number for sample rate value. 
exit 0
fi 

mkdir "$outdir"

for dir in "$indir"/*
do
	subDir=$(basename $dir)
	if test -f "$dir" # if it is file then create converted file directly in output directory
	then
       		sox "${dir%/}" --rate=$rateValue "$outdir"/"${subDir%.wav}"-"$rateValue".wav
      	fi

	if test -d "$dir" # if it is directory i.e. sub directory, then create a new directory in output 
	# directory with same name as input sub directory. And store converted files in new output sub 
	# directory.
	then
		mkdir "$outdir"/"$subDir"
		for track in "$dir"/*.wav
		do
			file=$(basename "$track")
			sox "$track" --rate=$rateValue "$outdir"/"$subDir"/"${file%.wav}"-"$rateValue".wav
		done
	fi
done
