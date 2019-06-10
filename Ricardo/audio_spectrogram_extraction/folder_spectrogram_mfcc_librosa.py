##########
### This script is used to generate a mfcc spectrogram
### Developed by Ricardo Reimao
### First argument: The path to the input folder (containing the original audio files)
### Second argument: The path for the output folder (which will contain the output spectrograms)
##########


from PIL import Image
import librosa
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import sys
import os
import numpy as np
from pathlib import Path

## Process input arguments
pathlist = Path(sys.argv[1]).glob('**/*.wav')
output_folder = sys.argv[2]
os.mkdir(output_folder)

## For loop to go through the folder and calculate the mfcc
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    y,sr = librosa.load(path_in_str)
    librosa_matrix = librosa.feature.mfcc(y=y,sr=sr,n_mfcc=128,fmax=8000)
    librosa_matrix = abs(librosa_matrix)  #Get absolute values
    librosa_matrix *= 255.0/librosa_matrix.max() #Normalizes the values between 0 and 255
    spec_image = Image.fromarray(librosa_matrix)
    output_filepath = output_folder + '/' + os.path.splitext(os.path.basename(path_in_str))[0] + '.bmp'
    print(output_filepath)
    spec_image.convert('RGB').save(output_filepath) 
print("Done!")

