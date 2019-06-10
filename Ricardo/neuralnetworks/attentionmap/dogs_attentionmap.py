#########################################
## CAM Attention Map Generator
## This tool generates an attention map for CNNs
## Created by Ricardo Reimao
## 16-Jan-2019
########################################

from keras.applications import VGG16
from keras.models import load_model
from vis.utils import utils
from keras import activations
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from vis.visualization import visualize_cam, overlay


###### VARIABLES ##########
img1_path = './img/dog.jpg'
img2_path = './img/dog2.jpg'
img3_path = './img/dog3.jpg'
output_path = 'output-dogs.jpg'
image_width = 224
image_height = 224
target_class_index = 208  #208 is the class of a labrador Fake
###########################




# Load model and load weights
model = VGG16(weights='imagenet', include_top=True)
print('>>> Model and Weights Loaded')

# Utility to search for layer index by name. 
# Alternatively we can specify this as -1 since it corresponds to the last layer.
layer_idx = -1 #utils.find_layer_idx(model, 'predictions')


# Swap softmax with linear
model.layers[layer_idx].activation = activations.linear
model = utils.apply_modifications(model)

# Loading images
plt.rcParams['figure.figsize'] = (18, 6)
img1 = utils.load_img(img1_path, target_size=(image_width, image_height))
img2 = utils.load_img(img2_path, target_size=(image_width, image_height))
img3 = utils.load_img(img3_path, target_size=(image_width, image_height))

# Showing image just to check if the load worked
#f, ax = plt.subplots(1, 2)
#ax[0].imshow(img1)
#ax[1].imshow(img2)
#plt.show()

# Preparing the plots
plt.figure()
f, ax = plt.subplots(1, 3)
plt.suptitle("CAM-Guided Mapping")

#Generates the CAM heatmap for image 1
grads = visualize_cam(model, layer_idx, filter_indices=target_class_index, seed_input=img1, backprop_modifier='guided') #208 is the class representing a Labrador

#Overlays the heatmap1 with the original image1
jet_heatmap = np.uint8(cm.jet(grads)[..., :3] * 255)
ax[0].imshow(overlay(jet_heatmap, img1))
print('>>> Heatmap 1 created')

#Generates the CAM heatmap for image 2
grads = visualize_cam(model, layer_idx, filter_indices=target_class_index, seed_input=img2, backprop_modifier='guided') #208 is the class representing a Labrador

#Overlays the heatmap1 with the original image1
jet_heatmap = np.uint8(cm.jet(grads)[..., :3] * 255)
ax[1].imshow(overlay(jet_heatmap, img2))
print('>>> Heatmap 2 created')

#Generates the CAM heatmap for image 3
grads = visualize_cam(model, layer_idx, filter_indices=target_class_index, seed_input=img3, backprop_modifier='guided') #208 is the class representing a Labrador

#Overlays the heatmap1 with the original image1
jet_heatmap = np.uint8(cm.jet(grads)[..., :3] * 255)
ax[2].imshow(overlay(jet_heatmap, img3))
print('>>> Heatmap 3 created')

# Show plot
plt.savefig(output_path)
print('>>> Output Image Saved')
plt.show()
