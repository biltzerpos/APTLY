import keras
import numpy as np
import tensorflow as tf
from keras.models import load_model


model = load_model('model.h5')
model.load_weights('inceptionv3_1.h5')

from pathlib import Path
import sys

flagged_ones = 0;
num_files = 0;

pathlist = Path(sys.argv[1]).glob('**/*.bmp')
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    image = tf.keras.preprocessing.image.load_img (path_in_str, target_size=(139,139))
    X = np.expand_dims(image, axis=0)
    predicted_class = model.predict(X)
    flagged_ones = flagged_ones + predicted_class
    num_files = num_files + 1
    print("Class: ", predicted_class)

print ("Amount of files: ", num_files);
print ("Sum: ", flagged_ones);
