
#!/bin/sh
# 17/07/2017
# This code is used to calculate RMS values of audio tracks. 
# It needs 2 arguments as input. First argument is input directory which contain wav files. And second argument is  
# output directory that you want to create.
# The input directory can have wav files or subfolders or both. For all the wav files it creates one text file.
# For all the subfolders, it creates separate text files for each folder. 

if test $# -ne 2
	then
	echo "You have entered $# arguments" 
   	echo "This script requires 2 arguments. See below for more..."$'\n'
	echo "%RMS"
	echo "Usage: RMS.sh <indir> <outdir>"
	echo "Enter name of input diretory as first argument, input directory should already exist and expected to have 
wav files"
	echo "Enter name of output directory as second argument, output directory must not exist before"
	exit 0
fi

indir="$1"
outdir="$2"

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
outfile="${2%/}"/"${1%/}".txt

touch "$outfile"
mkdir "$outdir"/"$indir"

for dir in "$indir"/*
	do
	subDir=$(basename $dir)
	if test -f "$dir"
	then
		file=$(basename "$dir")
		Avg=$(sox "$dir" -n stat 2>&1 | grep "RMS.* amplitude" | cut -d ":" -f 2)	
		echo "$file" : "RMS =" $Avg >> "$outfile"
	fi

	if test -d "$dir"	
	then
		for track in "$dir"/*.wav
		do
			dirOutfile="$2"/"$1"/"$subDir".txt
			touch "$dirOutfile"
			file=$(basename "$track")
			Avg=$(sox "$track" -n stat 2>&1 | grep "RMS.* amplitude" | cut -d ":" -f 2)
			echo "$file" : "RMS =" $Avg >> "$dirOutfile"
		done

	fi
done
