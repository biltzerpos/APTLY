#20/07/2017
# Equalize all the wav files in a given folder.

indir="$1"
outdir="$2"
gain="12"
width="1q"


if test $# -ne 2
        then
        echo "%equalizer"
        echo "Usage! equalizer.sh <indir> <outdir>"
	echo "Enter name of input directory as first argument"
        echo "Enter name of output directory as second argument"
        exit 0
fi

if test ! -d "indir"
then
echo "Input directory does not exist"
exit 0
fi


if test -d "$2"
then
echo "Output directory already exist, Please give another name for output directory"
exit 0
fi
mkdir "$2"

for track in "${indir%/}"/*.wav
do
echo "$track"
file=$(basename "$track")

sox -D "$track" "$outdir"/"${file%.wav}"-31.wav equalizer 31 $width $gain
sox -D "$track" "$outdir"/"${file%/.wav}"-63.wav equalizer 63 $width $gain
sox -D "$track" "$outdir"/"${file%/.wav}"-125.wav  equalizer 125 $width $gain
sox -D "$track" "$outdir"/"${file%/.wav}"-250.wav equalizer 250 $width $gain
sox -D "$track" "$outdir"/"${file%/.wav}"-500.wav equalizer 500 $width $gain
sox -D "$track" "$outdir"/"${file%/.wav}"-1k.wav equalizer 1k $width $gain
sox -D "$track" "$outdir"/"${file%/.wav}"-2k.wav equalizer 2k $width $gain
sox -D "$track" "$2"/"${file%/.wav}"-4k.wav equalizer 4k $width $gain
sox -D "$track" "$2"/"${file%/.wav}"-8k.wav equalizer 8k $width $gain
sox -D "$track" "$2"/"$file"-16k equalizer 16k $width $gain

done

