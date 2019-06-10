import os
import sys
import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras import optimizers

img_width = 87 #400
img_height = 504 #257

training_folder = sys.argv[1] # data/training
validation_folder = sys.argv[2] #data/validation


datagen = ImageDataGenerator()

train_generator = datagen.flow_from_directory(training_folder,
	target_size=(img_width, img_height),
	batch_size=16,
	class_mode='binary')

validation_generator = datagen.flow_from_directory(validation_folder,
	target_size=(img_width, img_height),
	batch_size=32,
	class_mode='binary')



#### Collecting data


##################### BEGIN MODEL ################################
model = Sequential()

#Layer1
model.add(Conv2D(32,(3,3), input_shape=(img_width, img_height, 3))) #32 filters of 3x3 size
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

#Layer2
model.add(Conv2D(32,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

#Layer3
model.add(Conv2D(64,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

#Fully Connected
model.add(Flatten())

#Fully Connected
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))

#Classifier Layer
model.add(Dense(1))
model.add(Activation('sigmoid'))
########################## END MODEL ##############################



### Compile the model
model.compile (loss='binary_crossentropy', optimizer='rmsprop', metrics=['binary_accuracy'])
model.save('model.h5')

### Train model
model.fit_generator(
	train_generator, 
	samples_per_epoch=6000, 
	nb_epoch=30, 
	validation_data=validation_generator, 
	nb_val_samples=1000)

##Save Model
model.save_weights('weights.h5')

