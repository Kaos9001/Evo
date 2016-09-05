import random
import numpy as np

class Creature:
	def __init__(self,layers,initial):
		self.position = [random.randint(0,800),random.randint(0,800)]
		self.velocity = [0,0]
		self.acceleration = [0.0,0.0]
		self.brain = Creature_Brain(layers,initial)
	def move(self,direction):
		possible = [(0,1),(0,-1),(1,0),(-1,0)]
		self.velocity = [self.velocity[x] + possible[direction][x] for x in range(2)]
		for num, item in enumerate(self.velocity):
			if item > 2:
				self.velocity[num] = 2
			elif item < -2:
				self.velocity[num] = -2
	def update(self):
		self.position = [self.position[x]+self.velocity[x] for x in range(2)]
		for num, item in enumerate(self.position):
			if item > 800:
				self.position[num] = 800
			elif item < 0:
				self.position[num] = 0

class Creature_Brain:
	def __init__(self,layers,initial=False):
		self.layers = self.make_layers(layers,initial)
	def make_layers(self,layer_scheme,initial):
		layers = []
		for num, amount in enumerate(layer_scheme[1:]):
			new = [Neuron() for _ in range(amount)]
			if initial:
				for n in new:
					n.set([random.random()*2-1 for x in range(layer_scheme[num])],random.random()*2-1)
			layers.append(new)
		return layers
	def think(self,inputs):
		current = inputs
		for layer in self.layers:
			current = [n.fire(current) for n in layer]
		return current
	def learn(self,variation):
		for layer in self.layers:
			current = [n.learn(variation) for n in layer]


class Neuron:
	def set(self,weights,bias):
		self.weights = weights
		self.bias = bias
	def fire(self,inputs):
		total = self.bias
		for i, value in enumerate(inputs):
			total += self.weights[i]*value
		return 1.0/(1+np.exp(-total))
	def learn(self,variation):
		self.weights = [x*(1-(random.random()*variation-variation/2)) for x in self.weights]
		self.bias += (random.random()*variation-variation/2)/100