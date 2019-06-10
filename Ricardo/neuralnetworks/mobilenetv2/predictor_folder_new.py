import keras
import numpy as np
import tensorflow as tf
from keras.models import load_model

###########
from tensorflow.python.keras._impl.keras.utils.generic_utils import CustomObjectScope
from tensorflow.python.keras._impl.keras.applications import mobilenet
from tensorflow.python.keras._impl.keras.models import load_model
with CustomObjectScope({'relu6': mobilenet.relu6,'DepthwiseConv2D': mobilenet.DepthwiseConv2D}):
    model = load_model('model.h5')
##########

#model = load_model('model.h5')a
model.load_weights('mobilenet_1.h5')

from pathlib import Path
import sys

flagged_ones = 0;
num_files = 0;

pathlist = Path(sys.argv[1]).glob('**/*.bmp')
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    image = tf.keras.preprocessing.image.load_img (path_in_str, target_size=(224,224))
    X = np.expand_dims(image, axis=0)
    predicted_class = model.predict(X)
    flagged_ones = flagged_ones + predicted_class
    num_files = num_files + 1
    print("Class: ", predicted_class)

print ("Amount of files: ", num_files);
print ("Sum: ", flagged_ones);
