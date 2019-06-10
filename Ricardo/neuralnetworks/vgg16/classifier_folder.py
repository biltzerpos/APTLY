import os
import sys
import keras
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras import optimizers
from keras.applications.vgg16 import VGG16

img_width = 224 #500
img_height = 224 #121

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
model = VGG16(weights='imagenet', include_top=False,input_shape=(img_width, img_height,3))

for layer in model.layers[:5]:
    layer.trainable = False

x = model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(1, activation="softmax")(x)
model_final = Model(input = model.input, output = predictions)
model_final.compile(loss = "binary_crossentropy", optimizer = optimizers.SGD(lr=0.0001, momentum=0.9), metrics=["binary_accuracy"])


##Layer1
#model.add(Conv2D(32,(3,3), input_shape=(img_width, img_height, 3))) #32 filters of 3x3 size
#model.add(Activation('relu'))
#model.add(MaxPooling2D(pool_size=(2,2)))
#
##Layer2
#model.add(Conv2D(32,(3,3)))
#model.add(Activation('relu'))
#model.add(MaxPooling2D(pool_size=(2,2)))
#
##Layer3
#model.add(Conv2D(64,(3,3)))
#model.add(Activation('relu'))
#model.add(MaxPooling2D(pool_size=(2,2)))
#
##Fully Connected
#model.add(Flatten())
#
##Fully Connected
#model.add(Dense(64))
#model.add(Activation('relu'))
#model.add(Dropout(0.5))
#
##Classifier Layer
#model.add(Dense(1))
#model.add(Activation('sigmoid'))

########################## END MODEL ##############################



### Compile the model
#model.compile (loss='binary_crossentropy', optimizer='rmsprop', metrics=['binary_accuracy'])
#model.compile(loss='binary_crossentropy', optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), metrics=['accuracy'])
model_final.save('model.h5')

### Train model
model_final.fit_generator(
	train_generator, 
	samples_per_epoch=6000, 
	nb_epoch=30, 
	validation_data=validation_generator, 
	nb_val_samples=1000)

##Save Model
model_final.save_weights('weights.h5')

