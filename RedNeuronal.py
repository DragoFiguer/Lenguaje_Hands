import cv2
import os
import numpy as np
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Ruta de los datos de entrenamiento y validación
datos_entrenamiento = 'C:\\Users\\figue\\Downloads\\ANIMALS\\Miniproyecto\\Entrenamiento'
datos_validacion = 'C:\\Users\\figue\\Downloads\\ANIMALS\\Miniproyecto\\Validacion'

iteraciones = 20
altura, longitud = 200, 200
batch_size = 1
pasos = 300 // 1
pasos_validacion = 300 // 1
filtrosconv1 = 32
filtrosconv2 = 64
filtrosconv3 = 128
tam_filtro1 = (4, 4)
tam_filtro2 = (3, 3)
tam_filtro3 = (2, 2)
tam_pool = (2, 2)
clases = 5
lr = 0.0005

prepocesamiento_entre = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True
)

preprocesamiento_vali = ImageDataGenerator(
    rescale=1./255
)

imagen_entreno = prepocesamiento_entre.flow_from_directory(
    datos_entrenamiento,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical',
)

imagen_validacion = preprocesamiento_vali.flow_from_directory(
    datos_validacion,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical',
)

cnn = Sequential()

cnn.add(Conv2D(filtrosconv1, tam_filtro1, padding='same', input_shape=(altura, longitud, 3)))
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(pool_size=tam_pool))

cnn.add(Conv2D(filtrosconv2, tam_filtro2, padding='same'))
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(pool_size=tam_pool))

cnn.add(Conv2D(filtrosconv3, tam_filtro3, padding='same'))
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(pool_size=tam_pool))

cnn.add(Flatten())
cnn.add(Dense(640))
cnn.add(Activation('relu'))
cnn.add(Dropout(0.5))
cnn.add(Dense(clases))
cnn.add(Activation('softmax'))

optimizar = tensorflow.keras.optimizers.Adam(learning_rate=lr)
cnn.compile(loss='categorical_crossentropy', optimizer=optimizar, metrics=['accuracy'])
cnn.fit(imagen_entreno, steps_per_epoch=pasos, epochs=iteraciones, validation_data=imagen_validacion, validation_steps=pasos_validacion)

cnn.save('ModeloVocales.h5')
cnn.save_weights('pesosVocales.h5')
