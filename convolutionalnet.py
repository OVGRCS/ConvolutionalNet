from google.colab import drive
drive.mount('/content/drive')

from matplotlib.pyplot import imshow
import numpy as np
from PIL import Image

# %matplotlib inline
pil_img = Image.open('X', 'r') #código para testear el acceso al directório de imágenes, sustituir X por la ruta a una imagen del dataset
imshow(np.asarray(pil_img))

import tensorflow as tf
tf.test.gpu_device_name()

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import keras
from time import time


# DATA SOURCE --------------------------------------------------

batch_size = 20

#En las siguientes dos líneas se importa el dataset desde directorio donde lo tenga localizado

train_data_dir = 'X' #Sustituir X por la dirección al dataset de entrenamiento
validation_data_dir = 'Y' #Sustituir Y por la dirección al dataset de validación

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='categorical')

# MODEL --------------------------------------------------

model = Sequential()
model.add(Conv2D(16, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(150, 150, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))

model.add(Dropout(0.5))
model.add(Dense(20, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

# TRAINING --------------------------------------------------

epochs = 100

h=model.fit_generator(
        train_generator,
        steps_per_epoch=150,
        epochs=epochs, 
        validation_data=validation_generator,
        validation_steps=800,
)
