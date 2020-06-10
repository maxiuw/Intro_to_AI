import cv2
import numpy as np
import os
import sys
import keras
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation,Flatten,Dense
from keras import optimizers
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # using gpu for the calculations
    config = tf.compat.v1.ConfigProto(device_count= {'GPU':1,'CPU':1})
    sess = tf.compat.v1.Session(config=config)
    tf.compat.v1.keras.backend.set_session(sess)

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = keras.utils.to_categorical(labels)

    # images = np.array(images)
    # images = images[np.newaxis,:,:,:]

    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    print(x_train[0])
    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    size = (IMG_WIDTH, IMG_HEIGHT)
    images = []
    label = []
    # entering the folder
    for root, folders, filenames in os.walk(data_dir):
        for folder in folders:
            file = os.listdir(os.path.join(root, folder))
            # image is an actual name of the file
            for image in file:
                imgFile = os.path.join(root, folder, image)
                # taking under account just images, there are also csv files in the dir
                if image[-4::] != '.ppm':
                    continue
                img = cv2.imread(imgFile)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # resizing the img to 30x30
                resize = cv2.resize(img, size)

                # appending info about img and labels under the same idx in 2 sept lists
                label.append(folder)
                images.append(resize)
    print('data was loaded\n')
    # print(np.array(images)[0].shape)
    return images,label


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = Sequential()
    # using 30 filters 6x6
    model.add(Conv2D(30,(6,6),input_shape=(IMG_WIDTH,IMG_HEIGHT,3),activation='relu'))
    # pooling layer - getting important info and making the size smaller
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(30, (3,3), activation='relu'))
    # pooling layer - getting important info and making the size smaller
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(30, (3, 3), activation='relu'))
    # pooling layer - getting important info and making the size smaller
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # flattening the output and generate output layer with probability for each class
    model.add(Flatten())
    model.add(Dense(NUM_CATEGORIES,activation='softmax'))
    opt = optimizers.Adam(lr=0.001)
    model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])
    print(model.summary())
    return model

if __name__ == "__main__":
    main()
