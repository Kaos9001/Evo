import scipy.special as sp
import random

class Neuron:
	def set(self,weights,bias):
		self.weights = weights
		self.bias = bias
	def fire(self,inputs):
		total = self.bias
		for i, value in enumerate(inputs):
			total += self.weights[i]*value
		return sp.expit(total)
	def variate(self,bias_variation,weight_variation):
		self.weights = [x + random.uniform(-weight_variation,weight_variation) for x in self.weights]
		self.bias += random.uniform(-bias_variation,bias_variation)

class Brain:
	def __init__(self,layer_scheme):
		self.layers = []
		self.scheme = layer_scheme
		self.make_layers(layer_scheme)
	def make_layers(self,layer_scheme):
		for num, amount in enumerate(layer_scheme[1:]):
			new = [Neuron() for _ in range(amount)]
			self.layers.append(new)
	def set_all_random(self,weight_boundary,bias_boundary):
		for index, layer in enumerate(self.layers):
			for neuron in layer:
				neuron.set([random.uniform(-weight_boundary,weight_boundary) for x in range(self.scheme[index])],random.uniform(-bias_boundary,bias_boundary))
	def process(self,inputs):
		for layer in self.layers:
			inputs = [n.fire(inputs) for n in layer]
		return inputs
	def variate_all(self,bias_variation,weight_variation):
		for layer in self.layers:
			for neuron in layer:
				neuron.variate(bias_variation,weight_variation)
	def get_layers_copy(self):
		copy = []
		for num_l, layer in enumerate(self.layers):
			copy.append([])
			for num_n, neuron in enumerate(layer):
				copy[num_l].append(Neuron())
				copy[num_l][num_n].set(self.layers[num_l][num_n].weights,self.layers[num_l][num_n].bias)
		return copy
