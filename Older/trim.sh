
#!/bin/sh
# 17/07/2017
# This code is used to trim the audio tracks from a given start time uptil specified length.
# It needs 4 arguments as input. First argument is input directory which contain wav files.
# Second argument is output directory that you want to create to store trimmed files.Third argument is
# the value at which you want to start trimming a file. Fourth argument is the length upto which you want 
# to trim.
# The input directory can have wav files or subfolders or both. For all the wav files it creates trimmed 
# file directly in the output folder. 
# For subfolders, it creates corresponding subfolders in output directory and create trimmed files in those 
# folders. 

if test $# -ne 4
        then
	echo "You have entered $# arguments" #changed
        echo "This script requires 4 arguments. See below for more..."$'\n'
        echo "%trim"
        echo "Usage: <indir> <outdir> <startValue> <length>"
	echo "Enter name of input diretory as first argument, input directory should exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist"
        echo "Enter the value at which you want to start trimming the song as third argument"
	echo "Enter the length upto which you want to trim the song after startig point e.g. if you want to 
trim the song from 30-50 sec then your third argument should be 30 (starting point) and fourth 
argument should be 20 (length after starting point)"
        exit 0
fi

indir="$1"
outdir="$2"
startValue="$3"
length="$4"

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


if [[ -z "$startValue" || $startValue == *[^[:digit:]]* ]]; then
echo Please enter a valid number for time at which you want to start trimming.
exit 0
fi


if [[ -z "$length" || $length == *[^[:digit:]]* ]]; then
echo Please enter a valid number for length of trimmed song.
exit 0
fi




mkdir "$outdir"


for dir in "$indir"/*
do
        subDir=$(basename $dir)
        if test -f "$dir" # if it is file then create trimmed file directly in output directory
        then
		sox "$dir" "${outdir%/}"/"${subDir%/}"-"$startValue"-"$length".wav trim "$startValue" "$Length"
        fi

        if test -d "$dir" # if it is directory i.e. sub directory, then create a new directory in output
        # directory with same name as input sub directory. And store trimmed files in new output sub
        # directory.
        then
                mkdir "$outdir"/"$subDir"
                for track in "$dir"/*.wav
                do
                        file=$(basename "$track")
			sox "$track" "$outdir"/"$subDir"/"$file"-"$startValue"-"$length".wav trim "$startValue" "$length"
                done
        fi
done
