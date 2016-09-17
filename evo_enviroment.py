import evo_graphic as evo_g
import evo_creature as evo_c
import random

class Better:
	def __init__(self,renderer):
		self.pop = {}
		self.types = {}
		self.renderer = renderer
	def populate(self,creatures):
		for pair in creatures:
			if pair[0].__name__ not in self.types.keys():
				self.types[pair[0].__name__] = pair[0]
				self.pop[pair[0].__name__] = []
			for _ in range(pair[1]):
				self.pop[pair[0].__name__].append(pair[0](pair[2],self))
				self.pop[pair[0].__name__][len(self.pop[pair[0].__name__])-1].randomize_brain()
	def update_all(self):
		for ctype in self.pop:
			for creature in self.pop[ctype]:
				creature.update()
	def get_best_of_type(self,ctype):
		chosen = random.random()*sum([x.fitness for x in self.pop[ctype]])
		total = 0
		for creature in self.pop[ctype]:
			total += creature.fitness
			if total >= chosen:
				return creature
		return self.get_oblg_best(ctype)
	def get_oblg_best(self,ctype):
		best = random.sample(self.pop[ctype],1)[0]
		for creature in self.pop[ctype]:
			if best.fitness <= creature.fitness:
				best = creature
		return best
	def refill(self,ctype):
		old = self.get_best_of_type(ctype)
		new = self.types[ctype](old.scheme,self)
		new.brain.layers = old.brain.get_layers_copy()
		new.brain.variate_all(50,10)
		new.color = tuple([max(30, min(255, x+random.randint(-10,10))) for x in old.color])
		self.pop[ctype].append(new)
	def get_nearest(self,creature):
		point = creature.position
		best = None
		smallest = 999999
		for other in self.pop[creature.__class__.__name__]:
			if other != creature:
				num = (creature.position[0]-other.position[0])**2+(creature.position[1]-other.position[1])**2
				if num < smallest:
					smallest = num
					best = other
		return best
	def check_collisions(self):
		for ctype in self.pop:
			for creature in self.pop[ctype]:
				if creature.fitness < creature.MINFITNESS:
					self.refill(creature.__class__.__name__)
					self.pop[ctype].remove(creature)
				other = self.get_nearest(creature)
				if creature.position[0] >= other.position[0] >= creature.position[0] - (creature.SIZE+other.SIZE) or creature.position[0] <= other.position[0] <= creature.position[0] + (creature.SIZE+other.SIZE):
					if creature.position[1] >= other.position[1] >= creature.position[1] - (creature.SIZE+other.SIZE) or creature.position[1] <= other.position[1] <= creature.position[1] + (creature.SIZE+other.SIZE):
						creature.fitness -= creature.PENALTY
						other.fitness -= other.PENALTY

display = evo_g.Renderer((1280,728))
test = Better(display)
test.populate([(evo_c.Ballie,20,[4,8,6,4]),(evo_c.Ballie2,50,[4,4,4,4])])

epsilon  = 10
while True:
	test.check_collisions()
	for ctype in test.pop:
		for bob in test.pop[ctype]:
			if random.randint(0,epsilon) == epsilon:
				bob.move(random.randint(0,3))
			else:
				near = test.get_nearest(bob).position
				r = bob.brain.process([bob.position[0],bob.position[1],bob.position[0]-near[0],bob.position[1]-near[1]])
				chosen = r.index(max(r))
				bob.move(chosen)
	test.update_all()
	display.update()