#########################################
## CAM Attention Map Generator
## This tool generates an attention map for CNNs
## Created by Ricardo Reimao
## 16-Jan-2019
########################################

from keras.models import load_model
from vis.utils import utils
from keras import activations
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from vis.visualization import visualize_cam, overlay


###### VARIABLES ##########
model_path = '/Users/ricardoreimao/Desktop/Masters/RESEARCH/NeuralNetworks/attentionmap/model_for2sec_soxmono_400.h5'
weights_path = '/Users/ricardoreimao/Desktop/Masters/RESEARCH/NeuralNetworks/attentionmap/vgg19_for2sec_soxmono_400.h5'
img1_path = './img/real1.bmp'
img2_path = './img/real2.bmp'
img3_path = './img/real3.bmp'
output_path = 'output.jpg'
image_width = 512
image_height = 250
target_class_index = 1  #0 is Fake, 1 is Real
###########################




# Load model and load weights
model = load_model(model_path)
print('>>> Model Loaded')
model.load_weights(weights_path)
print('>>> Weights Loaded')

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
#ax[2].yaxis.set_major_locator(plt.NullLocator())
#ax[2].xaxis.set_major_formatter(plt.NullFormatter())


# Show plot
plt.savefig(output_path)
print('>>> Output Image Saved')
plt.show()
