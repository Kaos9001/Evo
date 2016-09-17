import random
import numpy as np
import evo_neural as neural

class Creature:
	def constants(self):
		pass
	def __init__(self,layers,parent):
		self.MAX_SPEED = 3.0
		self.BRAIN_START_WEIGHTS_VAR = 10.0
		self.BRAIN_START_BIAS_VAR = 2.0
		self.SIZE = 10
		self.PENALTY = -10
		self.MINFITNESS = -200
		self.parent = parent
		self.position = [random.randint(0,self.parent.renderer.size[0]),random.randint(0,self.parent.renderer.size[1])]
		self.velocity = [0,0]
		self.scheme = layers
		self.brain = neural.Brain(layers)
		self.fitness = 0.0
		self.constants()
		self.speed = random.uniform(1,self.MAX_SPEED)
		self.color = (random.randint(30,255),random.randint(30,255),random.randint(30,255))
	def randomize_brain(self):
		self.brain.set_all_random(self.BRAIN_START_WEIGHTS_VAR,self.BRAIN_START_BIAS_VAR)
	def move(self,direction):
		possible = [(0,1),(0,-1),(1,0),(-1,0)]
		self.velocity = [possible[direction][0]*self.speed,possible[direction][1]*self.speed]
	def draw(self):
		self.parent.renderer.draw_dot([int(x) for x in self.position],self.SIZE,self.color)
	def update(self):
		self.physics_update()
		self.check_wall_collision()
		self.update_hook()
		self.draw()
	def update_hook(self):
		pass
	def physics_update(self):
		self.position = [self.position[x]+self.velocity[x] for x in range(2)]
	def check_wall_collision(self):
		for x in range(2):
			if self.position[x] > self.parent.renderer.size[x]-self.SIZE:
				self.position[x] = self.parent.renderer.size[x]-self.SIZE
				self.wall_collision_hook()
			if self.position[x] < self.SIZE:
				self.position[x] = self.SIZE
				self.wall_collision_hook()
	def wall_collision_hook(self):
		pass


class Ballie(Creature):
	def update_hook(self):
		self.fitness += 0.5
		self.fitness = min(100,self.fitness)
	def wall_collision_hook(self):
		self.fitness -= 10


class Ballie2(Creature):
	def update_hook(self):
		self.fitness += 0.25
		self.fitness = min(100,self.fitness)
	def wall_collision_hook(self):
		self.fitness -= 10
	def constants(self):
		self.SIZE = 7
		self.MAX_SPEED = 5
		self.PENALTY = -20