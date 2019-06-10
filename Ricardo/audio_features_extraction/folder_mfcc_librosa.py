##########
### This script is used to generate an average mfcc spectrogram vector given an audio file
### Developed by Ricardo Reimao
### First argument: The path to the input folder
### Second argument: The TAG of the file (eg. real or fake)
### Third argument: The path for the output file
### output CSV format: mfcc_bin1, mfcc_bin2, ..., class
##########


#import scipy.io.wavfile as wavfile
import librosa
#import scipy.signal as signal
import sys
import os
import numpy as np
from pathlib import Path

## Get folder from command line and load it using librosa
pathlist = Path(sys.argv[1]).glob('**/*.wav')
output_file_path = sys.argv[3]
output_file = open(output_file_path, "a+")

## Class of the file
class_folder = sys.argv[2]

## For loop to go through the folder and calculate the stft
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    y,sr = librosa.load(path_in_str,sr=None)
    librosa_matrix = librosa.feature.mfcc(y=y,sr=sr,n_mfcc=128) ## Librosa only support up to 128 MFCCs.
    average = np.average(librosa_matrix, axis=1)
    #i = 0
    for number in average:
        output_file.write(str('{:f}'.format(number.real)))
        #if i < len(average)-1:
        output_file.write(',')
        #    i += 1
    output_file.write(class_folder)
    output_file.write("\r\n")

output_file.close()
print("Done!")
