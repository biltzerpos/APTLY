#!/bin/sh

# 17/07/2017
# This code is used to chop a track into the segments of specific lengths. 
# It needs 3 arguments as input. First argument is full path of input track that you want to chop And second 
# argument is full path of output directory. You have to create output directory before running this code. The third 
# argument is the length segments in which you want to chop the songs.
# For each subfolder of input directory, you have to run the code again.

if test $# -ne 3  # 3 arguments are required to trim a track in intervals.  
	then
	echo "%Segments"
	echo "Usage: Segments.sh <inTrack> <outdir> <lengthSegment>"
	echo "Enter Full path of the input track as first argument"
	echo "Enter Full path to place chopped files as second argument"
	echo "Enter Required length of each chooped song as third argument" 
	exit 0
fi


if test ! -f "$1"
then
	echo "Input track does not exist"
	exit 0
fi


if test -d "$2"
then
	echo "Output directory already exist, Please give another name for output directory"
	exit 0
fi

trackPath="$1"
trackName=$(basename "$1")
start=0
interval=$3
time=$3

outdir="$2"
mkdir "$outdir"

length=`soxi -D "$trackPath"`


while test $interval -lt ${length%%.*} #convert float to int
do

	name=$(echo "$trackName" | cut -f 1 -d '.')  
	sox "$trackPath" "$outdir"/"$name"-"$start"-"$interval".wav trim "$start" "$time"
	start=`expr $start + $3`
	interval=`expr $interval + $3`
done

