##########
### This script is used to generate a stft spectrogram based on the SciPy library
### Developed by Ricardo Reimao
### First argument: The path to the input folder (containing the original audio)
### Second argument: The path for the output folder (which will contain the stft spectrograms)
###
### ** IMPORTANT ** : It is possible to generate stft spectrograms using SOX.
### The SoX tool is more reliable and generates the spectrogram quickier.
### Example of using sox for spectrograms:     sox input.wav -n spectrogram -m -r -o spectrogram.png
### First try to use SoX, it is the recommended method. Using this script is a backup plan in case SoX is not possible
##########


from PIL import Image
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

## For loop to go through the folder and calculate the stft
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    s,y = wavfile.read(path_in_str)
    a, b, stft_matrix = signal.stft(y,nperseg=512,nfft=2048)
    stft_matrix = abs(stft_matrix)  #Get absolute values
    stft_matrix *= 255.0/stft_matrix.max() #Normalizes the values between 0 and 255
    spec_image = Image.fromarray(stft_matrix)
    output_filepath = output_folder + '/' + os.path.splitext(os.path.basename(path_in_str))[0] + '.bmp'
    print(output_filepath)
    spec_image.convert('RGB').save(output_filepath) 
print("Done!")
