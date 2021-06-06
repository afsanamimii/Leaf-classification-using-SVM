# -*- coding: utf-8 -*-
"""svm to tflite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fsGZsUVbNbPy5nnS0fI_QSOAhrQ8l_Pp
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

from zipfile import ZipFile
import os
file_name="FINAL_THESIS_DATASET.zip"
with ZipFile(file_name,'r') as zip:
  zip.extractall()
  base_dir='/content/FINAL_THESIS_DATASET/NoyontaraandStrawberry'
  print("done")

#pre processing
IMAGE_SIZE = 224
BATCH_SIZE = 64

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True, 
    validation_split=0.1)


validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255, 
     validation_split=0.1 
                   )

train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE, 
    subset='training')

val_generator = validation_datagen .flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE, 
    subset='validation')

from tensorflow.keras.layers import Dense, Conv2D

from tensorflow.keras.regularizers import l2



cnn=tf.keras.Sequential()
cnn.add(tf.keras.layers.Conv2D(filters=32,padding='same',kernel_size=3,activation='relu',strides=2,input_shape=(224,224,3)))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=32,padding='same',kernel_size=3,activation='relu',strides=2))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=32,padding='same',kernel_size=3,activation='relu',strides=2))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=32,padding='same',kernel_size=3,activation='relu',strides=2))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))




cnn.add(tf.keras.layers.Flatten())
cnn.add(tf.keras.layers.Dense(units=128,activation='relu'))

cnn.add(Dense(4,kernel_regularizer=tf.keras.regularizers.l2(0.01),activation='softmax'))

from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping()

cnn.compile(optimizer='adam',loss='squared_hinge',metrics=['accuracy'])

history=cnn.fit(train_generator,validation_data=val_generator,epochs=10)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(6, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0.8,1.3])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()



saved_model_dir = 'savesvm/fine_tuning_n1'
tf.saved_model.save(cnn, saved_model_dir)

converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()

with open('modelsvm.tflite', 'wb') as f:
  f.write(tflite_model)

for image_batch, label_batch in train_generator:
  break
image_batch.shape, label_batch.shape

print (train_generator.class_indices)

labels = '\n'.join(sorted(train_generator.class_indices.keys()))

with open('labelsvm.txt', 'w') as f:
  f.write(labels)

loss, accuracy = cnn.evaluate(val_generator)