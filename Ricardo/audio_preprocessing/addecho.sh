#!/bin/sh
# 07/11/2018
# This code is used to apply echo to the audio tracks to a given value.
# It needs 3 arguments as input. First argument is input directory which contain wav files.
# Second argument is output directory that you want to create to store the processed files files.Third argument is 
# the value of the echo delay you will use for a echo effect.
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
        echo "%addecho"
	echo "Usage: addecho.sh <indir> <outdir> <volume>"
        echo "Enter name of input directory as first argument, input directory should already exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist before"
	echo "Enter the value to which you want to be the delay of the echo that will be applied to the tracks as third argument (Recommended 1000)"
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


#if -z "$rateValue"
#then
#echo Please enter a valid number for volume of noise. 
#exit 0
#fi 

mkdir "$outdir"

for dir in "$indir"/*
do
	subDir=$(basename $dir)
	if test -f "$dir" # if it is file then create converted file directly in output directory
	then
		sox "${dir%/}" "$outdir"/"${subDir%.wav}".wav echo 0.8 0.9 $rateValue 0.3 #echo gain-in gain-out <delay decay>
		#sox "${dir%/}" "$outdir"/"${subDir%.wav}".wav highpass $rateValue
      	fi

	if test -d "$dir" # if it is directory i.e. sub directory, then create a new directory in output 
	# directory with same name as input sub directory. And store converted files in new output sub 
	# directory.
	then
		mkdir "$outdir"/"$subDir"
		for track in "$dir"/*.wav
		do
			file=$(basename "$track")
			sox "$track" "$outdir"/"$subDir"/"${file%.wav}".wav echo 0.8 0.9 $rateValue 0.3
			#sox "$track" "$outdir"/"$subDir"/"${file%.wav}".wav highpass $rateValue
		done
	fi
done
