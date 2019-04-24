#17/07/2017
# This code is used to normalize a track at 8 different levels of loudness and then concatenate them to create one 
# long track. It takes 2 input arguments: input folder and name of output folder that you want to create. 

indir="$1"
outdir="$2"

if test $# -ne 2
        then
        echo "%normalize_concat"
        echo "Usage: normalize_concat.sh <indir> <outdir>"
	echo "Enter name of input diretory as first argument, input directory should already exist and expected to 
have wav files"
        echo "Enter name of output directory as second argument, output directory must not exist before"
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

x=`mktemp -d XXXXX`  

mkdir "$outdir"
for dir in "$indir"/*
do
	subDir=$(basename $dir)
	if test -f "$dir"
        then
                file=$(basename "$dir")
                 sox --norm=-35 "$dir" "$x"/"$file"-35.wav
                 sox --norm=-30 "$dir" "$x"/"$file"-30.wav
                 sox --norm=-25 "$dir" "$x"/"$file"-25.wav
                 sox --norm=-20 "$dir" "$x"/"$file"-20.wav
                 sox --norm=-15 "$dir" "$x"/"$file"-15.wav
                 sox --norm=-10 "$dir" "$x"/"$file"-10.wav
                 sox --norm=-5 "$dir" "$x"/"$file"-5.wav
                 sox --norm=-0 "$dir" "$x"/"$file"-0.wav
                 sox "$x"/"$file"-35.wav "$x"/"$file"-30.wav "$x"/"$file"-25.wav "$x"/"$file"-20.wav "$x"/"$file"-15.wav "$x"/"$file"-10.wav "$x"/"$file"-5.wav "$x"/"$file"-0.wav "$outdir"/"${file%.wav}"-Concat.wav
        fi

        if test -d "$dir"
        then
		mkdir "$outdir"/"$subDir"
		for track in "$dir"/*.wav	
		do
			file=$(basename "$track")
			sox --norm=-35 "$track" "$x"/"$file"-35.wav
			sox --norm=-30 "$track" "$x"/"$file"-30.wav
			sox --norm=-25 "$track" "$x"/"$file"-25.wav
			sox --norm=-20 "$track" "$x"/"$file"-20.wav
			sox --norm=-15 "$track" "$x"/"$file"-15.wav
			sox --norm=-10 "$track" "$x"/"$file"-10.wav
			sox --norm=-5 "$track" "$x"/"$file"-5.wav
			sox --norm=-0 "$track" "$x"/"$file"-0.wav
			sox "$x"/"$file"-35.wav "$x"/"$file"-30.wav "$x"/"$file"-25.wav "$x"/"$file"-20.wav "$x"/"$file"-15.wav "$x"/"$file"-10.wav "$x"/"$file"-5.wav "$x"/"$file"-0.wav "$outdir"/"$subDir"/"${file%.wav}"-Concat.wav
		done

	fi 
done

rm -rf "$x"
