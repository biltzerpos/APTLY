#!/bin/sh

# This code is used to convert stereo audios to mono
# It needs 2 arguments as input. First argument input directory that contain wav files. And 
# second argument is name output directory in which you want to store the modified wav files. 
# Created by Ricardo Reimao

indir="$1"
outdir="$2"

if test $# -ne 2  
        then
        echo "%stereotomono"
        echo "Usage: stereotomono.sh <indir> <outdir>"
	echo "Enter input directory that contains wav files as first argument"
        echo "Enter output directory to place the mono wav files as second argument, output directory must not exist before"
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
		if soxi "$dir" | grep 'Channels' | grep '2'; then
			sox "$dir" "${outdir%/}"/"$file1".wav remix 1,2
		else
			echo "Copying file..."
			cp "$dir" "${outdir%/}"/"$file1".wav
		fi
		#ffmpeg -i "$dir" "${outdir%/}"/"$file1".wav
        fi

        if test -d "$dir"
        then
                for track in "$dir"/*.mp3  ##original, wav
                do
                        dirOutfile="$folder"/"$subDir"
                        mkdir "$dirOutfile"
                        file=$(basename "$track")
			file1="${file%.wav}"
        	        if soxi "$dir" | grep 'Channels' | grep '2'; then
				sox "$track" "${dirOutfile%/}"/"$file1".wav remix 1,2
			else
				echo "Copying file..."
				cp "$dir" "${outdir%/}"/"$file1".wav
			fi
			#ffmpeg -i "$track" "${dirOutfile%/}"/"$file1".wav
		done
        fi
done

