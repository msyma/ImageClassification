from PIL import Image
import os
import glob
import random


DIR_FROM = ["database0//", "database1//"]
DIR_TO_TRAIN = "train_set//"
DIR_TO_TEST = "test_set//"
PATTERNS = ["car", "truck"]
TEST_TO_TRAIN_RATIO = 0.05

WIDTH = 160
HEIGHT = 120

def clean_files(dir_array):
    for directory in dir_array:
        files = glob.glob(directory + "*")

        for f in files:
            os.remove(f)

def get_number_of_image(directory):
    index = 0
    while True:
        try:
            image = open(str(directory) + str(index) + ".jpg")
        except IOError:
            break
        index += 1
        image.close()
    return index

def copy_image(filename, index, pattern, directory_from, directory_to):
    image = Image.open(directory_from + filename)
    image = image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    image.save(directory_to + pattern + str(index) + ".jpg")


### COPY
# dir_add = "new_truck//"
# dir_index = 1
# index_add = get_number_of_image(DIR_FROM[dir_index])
# files = glob.glob(dir_add + "*")
# for f in files:
#     image = Image.open(f)
#     # image = image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
#     image.save(DIR_FROM[dir_index] + str(index_add) + ".jpg")
#     index_add += 1


clean_files([DIR_TO_TRAIN, DIR_TO_TEST])

for index_set in range(len(PATTERNS)):
    image_number = get_number_of_image(DIR_FROM[index_set])

    index_train = 0
    index_test = 0
    for index in range(image_number):
        if random.random() > TEST_TO_TRAIN_RATIO:    
            copy_image(str(index) + ".jpg", index_train, PATTERNS[index_set], DIR_FROM[index_set], DIR_TO_TRAIN)
            index_train += 1

        else:
            copy_image(str(index) + ".jpg", index_test, PATTERNS[index_set], DIR_FROM[index_set], DIR_TO_TEST)
            index_test += 1
    