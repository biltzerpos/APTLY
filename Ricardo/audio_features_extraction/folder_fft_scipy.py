##########
### This script is used to generate the fft vector of files in a folder
### Developed by Ricardo Reimao
### First argument: The path to the input folder
### Second argument: The TAG of the file (eg. real or fake)
### Third argument: The path for the output file
### CSV output format: fft_bin1, fft_bin2, ..., fft_binN, class
##########


import scipy.io.wavfile as wavfile
from scipy.fftpack import fft
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
    fft_result = fft(y, n=1024)
    #a, b, stft_matrix = signal.stft(y,nperseg=2048) #change to 2048
    #average = np.average(stft_matrix, axis=1)
    for number in fft_result:
        output_file.write(str('{:f}'.format(number.real)))
        output_file.write(',')
    output_file.write(class_folder)
    output_file.write("\r\n")

output_file.close()
print("Done!")
