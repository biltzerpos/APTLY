##########
### This script is used to generate an average stft vector given an audio file
### Developed by Ricardo Reimao, based on previous work from Pedro Casas
##########


import librosa
import sys
import numpy as np


## Get file from command line and load it using librosa
filepath = sys.argv[1]
y,s = librosa.load(filepath)

## Calculate the STFT
stft_matrix = librosa.stft(y)
print("The variable y: ", y)
print("The variable s: ", stft_matrix)

## Average the whole matrix to get a vector
average = np.average(stft_matrix, axis=1)

## Print result
print("The variable average: ", average)
