
#!/bin/sh
# 17/07/2017
# This code is used to normalize the audio tracks to the given value.
# It needs 3 arguments as input. First argument is input directory which contain wav files.
# Second argument is output directory that you want to create to store normalized files.Third argument is 
# the value to which you want to normalize the tracks.
# The input directory can have wav files or subfolders or both. For all the wav files it creates one text 
# file.
# For all the subfolders, it creates separate text files for each folder.

indir="$1"
outdir="$2"
normValue="$3"

if test $# -ne 3
        then
	echo "You have entered $# arguments" 
        echo "This script requires 3 arguments. See below for more..."$'\n'
        echo "%normalize"
	echo "Usage: normalize.sh <indir> <outdir> <normValue>"
        echo "Enter name of input directory as first argument, input directory should already exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist before"
	echo "Enter the value to which you want to normalize the tracks as third argument"
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


if [[ -z "$normValue" || $normValue == *[^[:digit:]]* ]]; then
echo Please enter a valid number for normalization value. 
exit 0
fi 

mkdir "$outdir"

for dir in "$indir"/*
do
	subDir=$(basename $dir)
	if test -f "$dir" # if it is file then create normalized file directly in output directory
	then
       		sox --norm="$normValue" "${dir%/}" "$outdir"/"${subDir%.wav}"-Norm0.wav
      	fi

	if test -d "$dir" # if it is directory i.e. sub directory, then create a new directory in output 
	# directory with same name as input sub directory. And store normalized files in new output sub 
	# directory.
	then
		mkdir "$outdir"/"$subDir"
		for track in "$dir"/*.wav
		do
			file=$(basename "$track")
			sox --norm="$3" "$track" "$outdir"/"$subDir"/"${file%.wav}"-Norm0.wav
		done
	fi
done

