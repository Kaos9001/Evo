import random

class Creature:
	def __init__(self):
		self.position = [random.randint(0,800),random.randint(0,800)]
		self.velocity = [0,0]
		self.acceleration = [0.0,0.0]
	def move(self,direction):
		possible = [(0,1),(0,-1),(1,0),(-1,0)]
		self.velocity = [self.velocity[x] + possible[direction][x] for x in range(2)]
		for num, item in enumerate(self.velocity):
			if abs(item) > 2:
				self.velocity[num] = 2*((item<0)-(item>0))
	def update(self):
		self.position = [self.position[x]+self.velocity[x] for x in range(2)]
		for num, item in enumerate(self.position):
			if item > 800:
				self.position[num] = 800
			elif item < 0:
				self.position[num] = 0

