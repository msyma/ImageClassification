from PIL import Image
from itertools import product
import random


def get_number_of_image(directory, pattern):
    index = 0
    while True:
        try:
            image = open(str(directory) + pattern + str(index) + ".jpg")
        except IOError:
            break
        index += 1
        image.close()
    return index


class Database:

    def __init__(self, width, height, path_train_set, path_test_set, class_names=[]):
        self.width = width
        self.height = height
        self.path_train_set = path_train_set
        self.path_test_set = path_test_set
        self.calculated_index = 0
        self.calculated_class = 0

        self.train_set = []
        for class_name in class_names:
            self.train_set.append((class_name, get_number_of_image(path_train_set, class_name)))

        self.test_set = []
        for class_name in class_names:
            self.test_set.append((class_name, get_number_of_image(path_test_set, class_name)))

        print(self.train_set)
        print(self.test_set)


    def neuralDate(self, filePath, withEdit=False):
        image = Image.open(filePath)
        if withEdit:
            (width, height) = image.size
            image = image.rotate(random.randint(-8, 8))
            if random.randint(0, 1):
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            widthRate = int(0.05 * width)
            heightRate = int(0.05 * height)
            image = image.crop((random.randint(0, widthRate), random.randint(0, heightRate), \
                                width - random.randint(0, widthRate), height - random.randint(0, heightRate)))

        image = image.resize((self.width, self.height), Image.ANTIALIAS)
        # image.save("res1.jpg")

        array_image = image.load()
        # print(image.size, self.width, self.height, filePath)
        array = [ [ sum(image.getpixel((x, y))) / 765 for x in range(self.width) ] for y in range(self.height) ]
        image.close()
        return array

    def get(self):
        set_to_open = random.randint(0, len(self.train_set) -1)

        index = random.randint(0, self.train_set[set_to_open][1] -1)

        filePath = self.path_train_set + self.train_set[set_to_open][0] + str(index) + '.jpg'
        return (self.neuralDate(filePath, True), self.train_set[set_to_open][0])

    def check_answer(self, reset=False):
        if reset:
            self.calculated_index = 0
            self.calculated_class = 0

        if self.calculated_index >= self.test_set[self.calculated_class][1]:
            self.calculated_class += 1
            self.calculated_index = 0
            if self.calculated_class >= len(self.test_set):
                return False, False

        self.calculated_index += 1
        path = self.path_test_set \
            + self.test_set[self.calculated_class][0] \
            + str(self.calculated_index -1)

        return (self.neuralDate(path + '.jpg'), self.test_set[self.calculated_class][0], path)


    def make_foto(self, array, width = None, height = None):
        if width == None and height == None:
            width = self.width
            height = self.height

        image = Image.new('RGB', (width, height), color = 'black')
        array_image = image.load()
        for (y, x) in product(range(height), range(width)):
            value = int(array[y][x] * 765 / 3)
            array_image[x, y] = (value, value, value)
        image.save("res.jpg")

    def flat_array(self, array, make_foto = False):
        width = len(array[0])
        height = len(array)
        if make_foto:
            self.make_foto(array, width, height)
        arr = [0 for i in range(width * height)]
        for y in range(height):
            for x in range(width):
                arr[x * height + y] = array[y][x]
        return arr
