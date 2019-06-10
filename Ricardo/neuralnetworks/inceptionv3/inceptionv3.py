from keras import applications
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model 
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as k 
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
import sys


img_width = 139 #400 #139 #400 #500 #256 
img_height = 139 #257 #504 #257 #139 #256, 256

train_data_dir = sys.argv[1]
validation_data_dir = sys.argv[2]
nb_train_samples = 4125
nb_validation_samples = 500 
batch_size = 16
epochs = 50


####Choosing the model
model = InceptionV3(weights = "imagenet", include_top=False, input_shape = (img_height,img_width, 3))



# Freeze the layers which you don't want to train.
for layer in model.layers[:249]:   #249 means to freeze everything except the top 2 inception blocks
    layer.trainable = False

#Adding custom Layers 
x = model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
#x = Dense(1024, activation="relu")(x)
predictions = Dense(2, activation="softmax")(x)

# creating the final model 
model_final = Model(input = model.input, output = predictions)

# compile the model 
model_final.compile(loss = "categorical_crossentropy", optimizer='rmsprop', metrics=["accuracy"])
model_final.save('model.h5')

# Initiate the train and test generators with data Augumentation 
train_datagen = ImageDataGenerator(
#rescale = 1./255,
#horizontal_flip = True,
#fill_mode = "nearest",
#zoom_range = 0.3,
#width_shift_range = 0.3,
#height_shift_range=0.3,
#rotation_range=30
)

test_datagen = ImageDataGenerator(
#rescale = 1./255,
#horizontal_flip = True,
#fill_mode = "nearest",
#zoom_range = 0.3,
#width_shift_range = 0.3,
#height_shift_range=0.3,
#rotation_range=30
)

train_generator = train_datagen.flow_from_directory(
train_data_dir,
target_size = (img_height, img_width),
batch_size = batch_size, 
class_mode = "categorical")

validation_generator = test_datagen.flow_from_directory(
validation_data_dir,
target_size = (img_height, img_width),
class_mode = "categorical")

# Save the model according to the conditions  
checkpoint = ModelCheckpoint("inceptionv3_1.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=10, verbose=1, mode='auto')


# Train the model 
model_final.fit_generator(
train_generator,
samples_per_epoch = nb_train_samples,
epochs = epochs,
validation_data = validation_generator,
nb_val_samples = nb_validation_samples,
callbacks = [checkpoint, early])

