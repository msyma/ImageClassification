from PIL import Image
import graphics
import time
import math
import random

RADIOUS = 10
WIDTH = 1200
HEIGHT = 900


def value_to_color(value):
	return graphics.color_rgb(int(value * 255), int(value * 255), int(value * 255))

def value_to_color_line(value):
	if value > 0:
		value = int((1 - min(value, 1)) * 255)
		return graphics.color_rgb(255, value, value)
	else:
		value = int((1 + max(value, -1)) * 255)
		return graphics.color_rgb(value, value, 255)

def make_line(point_a, point_b):
	a = - (point_b.getY() - point_a.getY()) / (point_b.getX() - point_a.getX())
	k = math.sqrt(pow(RADIOUS, 2) / (1 + pow(a, 2)))

	point_new_a = graphics.Point(point_a.getX() + k, point_a.getY() - a * k)
	point_new_b = graphics.Point(point_b.getX() - k, point_b.getY() + a * k)

	return graphics.Line(point_new_a, point_new_b)



class Visualizer:

	def __init__(self, network):
		self.window = graphics.GraphWin("Network" + network.name, WIDTH, HEIGHT)
		self.neurons = [ [] for _ in range(network.size)]
		self.image = None


		graphics.Text(graphics.Point(WIDTH / (network.size + 1) + 32, HEIGHT//2), ". . .").draw(self.window)
		for layer in range(network.size):
			for n in range(network.setup[layer]):
				if layer + 1 == network.size and n + 1 == network.setup[layer]:
					break

				point = graphics.Point((layer + 1) * (WIDTH / (network.size + 1)),
					(n + 1) * (HEIGHT / (network.setup[layer] + 1)))

				circle = graphics.Circle(point, RADIOUS)
				circle.draw(self.window)

				if layer + 1 == network.size and n + 1 < network.setup[layer]:
					print(n, network.class_names)
					(graphics.Text(graphics.Point
						(point.getX() + 32, point.getY()), network.class_names[n])).draw(self.window)

				lines = []
				if layer > 1: # > 0		
					for line_num in range(network.setup[layer - 1]):
						lines.append(make_line(
							self.neurons[layer - 1][line_num][0], point))
						lines[line_num].setWidth(2)
						lines[line_num].draw(self.window)

				self.neurons[layer].append((point, circle, lines))
				
		

	def refresh(self, network, path=None):
		for layer_num in range(len(self.neurons)):
			for neuron_num in range(len(self.neurons[layer_num])):
				if layer_num + 1 == len(self.neurons) and neuron_num == len(self.neurons[layer_num]):
					break;

				self.neurons[layer_num][neuron_num][1].setFill(
					value_to_color(network.values[layer_num][neuron_num]))

				# print(self.neurons[layer_num][neuron_num][2], len(self.neurons[layer_num][neuron_num][2]))
				for line_num in range(len(self.neurons[layer_num][neuron_num][2])):

					self.neurons[layer_num][neuron_num][2][line_num].setOutline(
						value_to_color_line(network.layers[layer_num][line_num][neuron_num]))

		if path != None:
			image = Image.open(path + ".jpg")
			(width, height) = image.size
			image = image.resize((2 * width, 2 * height), Image.ANTIALIAS)
			image.save("out.gif")
			self.image = graphics.Image(
				graphics.Point(width, height), "out.gif")
			self.image.draw(self.window)

		else:
			if self.image != None:
				self.image.undraw(self.window)
				self.image = None

		self.window.getMouse()

	def close(self):
		self.window.getMouse()
		self.window.close()
