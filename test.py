import os
import cv2
IMG_WIDTH = 30
IMG_HEIGHT = 30

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
                print(folder)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # print(image[0:4])
                label.append(image[0:5])
                resize = cv2.resize(img, size)
                # print('resize',image)
                # print(img.shape)
                images.append(resize)
    print('data was loaded\n')
    # print(np.array(images)[0].shape)
    return images,label

img,lb = load_data('Images')
print(lb)