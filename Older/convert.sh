#!/bin/sh

# 17/07/2017
# This code is used to convert mp3 files to wav files.
# It needs 2 arguments as input. First argument input directory that contain mp3 files. And 
# second argument is name output directory in which you want to store wav files. 

indir="$1"
outdir="$2"

if test $# -ne 2  
        then
	echo "You have entered $# arguments" 
   	echo "This script requires 2 arguments. See below for more..."$'\n'
        echo "%convert"
        echo "Usage: convert.sh <indir> <outdir>"
	echo "Enter input directory that contains mp3 files as first argument"
        echo "Enter output directory to place wav files as second argument, output directory must not exist before"
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

mkdir "$outdir"
folder="${outdir%/}"/"$(basename $indir)"
mkdir "$folder"


for dir in "$indir"/*
do
        subDir=$(basename $dir)
        if test -f "$dir"
        then
                file=$(basename "$dir")
                file1="${file%.mp3}"
	        ffmpeg -i "$dir" "${outdir%/}"/"$file1".wav
        fi

        if test -d "$dir"
        then
                for track in "$dir"/*.wav
                do
                        dirOutfile="$folder"/"$subDir"
                        mkdir "$dirOutfile"
                        file=$(basename "$track")
			file1="${file%.mp3}"
        	        ffmpeg -i "$track" "${dirOutfile%/}"/"$file1".wav
		done
        fi
done

