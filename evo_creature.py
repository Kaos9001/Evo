import random
import numpy as np
import scipy.special as s

class Creature:
	def __init__(self,layers,initial):
		self.position = [random.randint(0,800),random.randint(0,800)]
		self.velocity = [0,0]
		self.acceleration = [0.0,0.0]
		self.data = (layers,initial)
		self.brain = Creature_Brain(layers,initial)
		self.fitness = 0.0
	def move(self,direction):
		possible = [(0,0.1),(0,-0.1),(0.1,0),(-0.1,0)]
		self.velocity = [self.velocity[x] + possible[direction][x] for x in range(2)]
		for num, item in enumerate(self.velocity):
			if item > 2:
				self.velocity[num] = 2
			elif item < -2:
				self.velocity[num] = -2
	def update(self):
		self.position = [self.position[x]+self.velocity[x] for x in range(2)]
		a = (abs(self.position[0]-400)+abs(self.position[1]-400))
		if a == 0:
			a = 1
		self.fitness += 5.0/a
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
	def learn(self,variation,check,variationB):
		for layer in self.layers:
			current = [n.learn(variation,check,variationB) for n in layer]
	def copy(self):
		copy = []
		for num_l, layer in enumerate(self.layers):
			copy.append([])
			for num_n, neuron in enumerate(layer):
				copy[num_l].append(Neuron())
				copy[num_l][num_n].set(self.layers[num_l][num_n].weights,self.layers[num_l][num_n].bias)
		return copy


class Neuron:
	def set(self,weights,bias):
		self.weights = weights
		self.bias = bias
	def fire(self,inputs):
		total = self.bias
		for i, value in enumerate(inputs):
			total += self.weights[i]*value
		return s.expit(total)
	def learn(self,variation,check,variationB):
		self.weights = [x+(random.random()*variation-variation/2) if random.randint(0,check) == 0 else x for x in self.weights ]
		self.bias += (random.random()*variationB-variationB/2)