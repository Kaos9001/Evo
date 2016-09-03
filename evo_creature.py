import random

class Creature:
	def __init__(self):
		self.position = (random.randint(0,800),random.randint(0,800))
		self.velocity = (0,0)
	def move(self,direction):
		possible = [(0,1),(0,-1),(1,0),(-1,0)]
		self.velocity = possible[direction]
	def update(self):
		self.position = [self.position[x]+self.velocity[x] for x in range(2)]