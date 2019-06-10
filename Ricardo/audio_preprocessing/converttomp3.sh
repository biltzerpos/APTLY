#!/bin/sh

# 17/07/2017
# This code is used to convert wav files to mp3 files.
# It needs 2 arguments as input. First argument input directory that contain wav files. And 
# second argument is name output directory in which you want to store mp3 files. 

indir="$1"
outdir="$2"

if test $# -ne 2  
        then
        echo "%convert"
        echo "Usage: convert.sh <indir> <outdir>"
	echo "Enter input directory that contains wav files as first argument"
        echo "Enter output directory to place mp3 files as second argument, output directory must not exist before"
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
                file1="${file%.wav}"
		ffmpeg -i "$dir" "${outdir%/}"/"$file1".mp3
        fi

        if test -d "$dir"
        then
                for track in "$dir"/*.wav  ##original, wav
                do
                        dirOutfile="$folder"/"$subDir"
                        mkdir "$dirOutfile"
                        file=$(basename "$track")
			file1="${file%.wav}"
        	        ffmpeg -i "$track" "${dirOutfile%/}"/"$file1".mp3
		done
        fi
done

