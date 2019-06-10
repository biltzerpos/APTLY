import keras
import numpy as np
import tensorflow as tf
from WaveNetClassifier import WaveNetClassifier
import sys
import librosa
from pathlib import Path

duration_audio = 5 # 16000 samples per second X 5 seconds
sample_rate = 16000

training_folder = sys.argv[1] # data/training
validation_folder = sys.argv[2] #data/validation


######################## BUILDING DATASET ############################
X_training = np.zeros(duration_audio*sample_rate)
Y_training = np.zeros(1)
X_validation = np.zeros(duration_audio*sample_rate)
Y_validation = np.zeros(1)

## Collect training_folder data
pathlist = Path(training_folder).glob('fake/*.wav')
for path in pathlist:
    path_in_str = str(path)
    audio_content,sample_rate = librosa.core.load(path_in_str, sr=sample_rate, mono=True, offset=0.0, duration=duration_audio)
    audio_content.resize(duration_audio*sample_rate, refcheck=False)
    X_training = np.vstack((X_training,audio_content))
    Y_training = np.vstack((Y_training,1))

pathlist = Path(training_folder).glob('real/*.wav')
for path in pathlist:
    path_in_str = str(path)
    audio_content,sample_rate = librosa.core.load(path_in_str, sr=sample_rate, mono=True, offset=0.0, duration=duration_audio)
    audio_content.resize(duration_audio*sample_rate, refcheck=False)
    X_training = np.vstack((X_training,audio_content))
    Y_training = np.vstack((Y_training,0))

X_training = np.delete(X_training, (0), axis=0)
Y_training = np.delete(Y_training, (0), axis=0)
print('Size of Training Set - X: ' + str(len(X_training))+ ' - Y: ' + str(len(Y_training)))


## Collect validation_folder data
pathlist = Path(validation_folder).glob('fake/*.wav')
for path in pathlist:
    path_in_str = str(path)
    audio_content,sample_rate = librosa.core.load(path_in_str, sr=sample_rate, mono=True, offset=0.0, duration=duration_audio)
    audio_content.resize(duration_audio*sample_rate, refcheck=False)
    X_validation = np.vstack((X_validation,audio_content))
    Y_validation = np.vstack((Y_validation,1))

pathlist = Path(validation_folder).glob('real/*.wav')
for path in pathlist:
    path_in_str = str(path)
    audio_content,sample_rate = librosa.core.load(path_in_str, sr=sample_rate, mono=True, offset=0.0, duration=duration_audio)
    audio_content.resize(duration_audio*sample_rate, refcheck=False)
    X_validation = np.vstack((X_validation,audio_content))
    Y_validation = np.vstack((Y_validation,0))

X_validation = np.delete(X_validation, (0), axis=0)
Y_validation = np.delete(Y_validation, (0), axis=0)
print('Size of Validation Set: X: ' + str(len(X_validation))+ ' - Y: ' + str(len(Y_validation)))
####################################################################


################ Build and train model #############################
model = WaveNetClassifier((80000,), (1,), kernel_size = 2, dilation_depth = 9, n_filters = 40, task = 'classification')
model.fit(X_training, Y_training, validation_data = (X_validation, Y_validation), epochs = 100, batch_size = 32, optimizer='adam', save=True, save_dir='./')

