#!/bin/sh
# 07/11/2018
# This code is used to apply white noise to the audio tracks to a given value.
# It needs 3 arguments as input. First argument is input directory which contain wav files.
# Second argument is output directory that you want to create to store the processed files files.Third argument is 
# the value of the volume of the noise you will use for a highpass filter.
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
        echo "%addnoise"
	echo "Usage: addnoise.sh <indir> <outdir> <volume>"
        echo "Enter name of input directory as first argument, input directory should already exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist before"
	echo "Enter the value to which you want to be the volume of the noise that will be applied to the tracks as third argument (Recommended 0.02)"
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
       		sox "${dir%/}" -p synth whitenoise vol $rateValue | sox -m "${dir%/}" - "$outdir"/"${subDir%.wav}".wav
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
			sox "$track" -p synth whitenoise vol $rateValue | sox -m "$track" - "$outdir"/"$subDir"/"${file%.wav}".wav
			#sox "$track" "$outdir"/"$subDir"/"${file%.wav}".wav highpass $rateValue
		done
	fi
done
