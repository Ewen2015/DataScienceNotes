import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (10,10)
mpl.rcParams['axes.grid'] = False

import numpy as np
from PIL import Image
import time
import functools

import tensorflow as tf
# from tensorflow.keras.preprocessing import image as kp_image
# from tensorflow.keras import models 
# from tensorflow.keras import losses
# from tensorflow.keras import layers
# from tensorflow.keras import backend as K

def load_resize_img(path, max_dim=512):
    img = Image.open(path)
    
    long = max(img.size)
    scale = max_dim/long
    
    img = img.resize((round(img.size[0]*scale), round(img.size[1]*scale)), Image.ANTIALIAS)
    img_array = tf.keras.preprocessing.image.img_to_array(img)

    # We need to broadcast the image array such that it has a batch dimension 
    img_array = np.expand_dims(img, axis=0)
    return img_array

def display_img(img_array, title=None):
    # Remove the batch dimension
    out = np.squeeze(img_array, axis=0)
    # Normalize for display 
    out = out.astype('uint8')
    plt.imshow(out)
    if title:
        plt.title(title)
    return None


import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (10,10)
mpl.rcParams['axes.grid'] = False

import numpy as np
from PIL import Image
import time
import functools

import tensorflow as tf
# from tensorflow.keras.preprocessing import image as kp_image
# from tensorflow.keras import models 
# from tensorflow.keras import losses
# from tensorflow.keras import layers
# from tensorflow.keras import backend as K

def load_resize_img(path, max_dim=512):
    img = Image.open(path)
    
    long = max(img.size)
    scale = max_dim/long
    
    img = img.resize((round(img.size[0]*scale), round(img.size[1]*scale)), Image.ANTIALIAS)
    img_array = tf.keras.preprocessing.image.img_to_array(img)

    # We need to broadcast the image array such that it has a batch dimension 
    img_array = np.expand_dims(img, axis=0)
    return img_array

def display_img(img_array, title=None):
    # Remove the batch dimension
    out = np.squeeze(img_array, axis=0)
    # Normalize for display 
    out = out.astype('uint8')
    plt.imshow(out)
    if title:
        plt.title(title)
    return None


# Content layer where will pull our feature maps
content_layers = ['block5_conv2'] 

# Style layer we are interested in
style_layers = ['block1_conv1',
                'block2_conv1',
                'block3_conv1', 
                'block4_conv1', 
                'block5_conv1']

num_content_layers = len(content_layers)
num_style_layers = len(style_layers)

vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
vgg.trainable = False

# Get output layers corresponding to style and content layers 
style_outputs = [vgg.get_layer(name).output for name in style_layers]
content_outputs = [vgg.get_layer(name).output for name in content_layers]
model_outputs = style_outputs + content_outputs

model = tf.keras.Model(inputs=vgg.input, outputs=model_outputs, name='style transfer')
for layer in model.layers:
    layer.trainable = False
    





