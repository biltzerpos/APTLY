#########################################
## CAM Attention Map Generator - AVERAGE activation map
## This tool generates an average attention map for CNNs
## Created by Ricardo Reimao
## 30-Jan-2019
########################################

from keras.models import load_model
from vis.utils import utils
from keras import activations
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
import keras
from vis.visualization import visualize_cam, overlay
import sys
import os
from pathlib import Path
## EXTRA FROM MOBILENET ##
from keras.utils.generic_utils import CustomObjectScope

#from tensorflow.python.keras._impl.keras.utils.generic_utils import CustomObjectScope
#from tensorflow.python.keras._impl.keras.applications import mobilenet
#from tensorflow.python.keras._impl.keras.models import load_model


###### VARIABLES ##########
model_path = './mobilenet_model_forrerecorded_cqt_87.h5'
weights_path = './mobilenet_weights_forrerecorded_cqt_87.h5'
folder_path = './img/for-rerecording-cqt-testing/fake'
output_path = './output/output_average_fake_validation_rerecorded_cqt.jpg'
image_width = 244 #400 #200
image_height = 244 #257 #121
target_class_index = 0  #0 is Fake, 1 is Real
plot_title = 'CAM-Guided Mapping: Average Activation Map for Unseen Synthetic Speech (for-rerecorded)'
###########################

#######CUTSOM FROM MOBILENET###############
#with CustomObjectScope({'relu6': mobilenet.relu6,'DepthwiseConv2D': mobilenet.DepthwiseConv2D}):
with CustomObjectScope({'relu6': keras.layers.ReLU(6.),'DepthwiseConv2D': keras.layers.DepthwiseConv2D}):
    model = load_model(model_path)
##########################################



# Load model and load weights
#model = load_model(model_path)
print('>>> Model Loaded')
model.load_weights(weights_path)
print('>>> Weights Loaded')

# Utility to search for layer index by name. 
# Alternatively we can specify this as -1 since it corresponds to the last layer.
layer_idx = -1 #utils.find_layer_idx(model, 'predictions')


# Swap softmax with linear
model.layers[layer_idx].activation = activations.linear
model = utils.apply_modifications(model)


# Reading file paths
pathlist = Path(folder_path).glob('**/*.bmp')
pathlist2 = Path(folder_path).glob('**/*.bmp')
amount_files = len(list(pathlist2))
print('Amount of files found: ' + str(amount_files))

# Preparing the plot
plt.rcParams['figure.figsize'] = (18, 6)
plt.figure()
plt.suptitle(plot_title)

#Creating an empty averaged attention map
average_grads = np.zeros((image_width,image_height))

# Iteracting through the files and generating the average attention map
file_counter = 1
for path in pathlist:
	# Preparing the plots
	path_in_str = str(path)
	print('>>> File [' + str(file_counter) + '/'+ str(amount_files) +']: ' + path_in_str)
	img = utils.load_img(path_in_str, target_size=(image_width, image_height))
	grads = visualize_cam(model, layer_idx, filter_indices=target_class_index, seed_input=img, backprop_modifier='guided')
	average_grads = average_grads + (grads/amount_files)
	file_counter = file_counter + 1

#Creating the heatmap based on the averaged attention map
jet_heatmap = np.uint8(cm.jet(average_grads)[..., :3] * 255)

#Saving the plot
plt.imshow(jet_heatmap)
plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

print('>>> DONE')
