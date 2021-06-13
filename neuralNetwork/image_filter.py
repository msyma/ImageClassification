import random
from enum import Enum

def sum_array(A, B):
	for b in B:
		A.append(b)
	return A

def sum_array_all(array):
	result = array[0]
	for i in range(1, len(array)):
		result = sum_array(result, array[i])
	return result


class Pooling_Type(Enum):
	MAX = 1
	AVG = 2


class Individual_Filter:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.values = [[random.random() for x in range(width)] for y in range(height)]

	def cell_calculate(self, array, x, y):
		array_width = len(array[0])
		array_height = len(array)
		value = 0
		for y_filter in range(self.height):
			for x_filter in range(self.width):
				if x + x_filter < array_width and y + y_filter < array_height:
					value += array[y + y_filter][x + x_filter] * self.values[y_filter][x_filter]
		return min(1, max(value, 0))


	def process(self, array):
		array_width = len(array[0])
		array_height = len(array)
		new_array = [[0 for x in range(array_width)] for y in range(array_height)]

		for y_height in range(array_height):
			for x_width in range(array_width):
				new_array[y_height][x_width] = self.cell_calculate(array, x_width, y_height)
		return pooling(new_array, 2, 2, Pooling_Type.MAX)


def pooling(array, width, height, pooling_type = Pooling_Type.MAX):
	array_width = len(array[0])
	array_height = len(array)
	new_array = [[0 for x in range(int((array_width + width - 1) / width))] for y in range(int((array_height + height - 1) / height))]

	for y_height in range(array_height):
		for x_width in range(array_width):
			if pooling_type == Pooling_Type.MAX:
				new_array[int(y_height / height)][int(x_width / width)] = \
					max(new_array[int(y_height / height)][int(x_width / width)], array[y_height][x_width])

			if pooling_type == Pooling_Type.AVG:
				new_array[int(y_height / height)][int(x_width / width)] += array[y_height][x_width]
				if x_width % width == width -1 and y_height % height == height -1:
					new_array[int(y_height / height)][int(x_width / width)] /= width * height
	return new_array


class Set_Filter:
    
	def __init__(self, filter_array):
		self.filter_array = filter_array

	def __call__(self, image, layer=0):
		if layer == 0:
			image = [image]

		if layer >= len(self.filter_array):
			return sum_array_all(image)

		result = []
		for i in image:
			for f in self.filter_array[layer]:
				result.append(f.process(i))

		return self(result, layer +1)


