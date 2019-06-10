##########
### This script is used to generate an average stft vector given an audio file
### Developed by Ricardo Reimao, based on previous work from Pedro Casas
### First argument: The path to the input folder
### Second argument: The TAG of the file (eg. real or fake)
### Third argument: The path for the output file
##########


import scipy.io.wavfile as wavfile
import scipy.signal as signal
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
    s,y = wavfile.read(path_in_str)
    a, b, stft_matrix = signal.stft(y,nperseg=2048) #change to 2048
    average = np.average(stft_matrix, axis=1)
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
