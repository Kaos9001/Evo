import evo_graphic as evo_g
import evo_creature as evo_c
import random

class Enviroment:
	def __init__(self,renderer):
		self.renderer = renderer
		self.nearest = {}
		self.pop = []
	def populate(self,creature):
		self.pop.append(creature)
	def update_all(self):
		for creature in self.pop:
			self.draw_creature(creature)
			creature.update()
	def draw_creature(self,creature):
		self.renderer.draw_dot([int(x) for x in creature.position],10,(255,0,0))
	def get_nearest(self,creature):
		point = creature.position
		best = None
		smallest = 999999
		for other in self.pop:
			if other != creature:
				num = (creature.position[0]-other.position[0])**2+(creature.position[1]-other.position[1])**2
				if num < smallest:
					smallest = num
					best = other
		return best
	def check_for_deaths(self):
		for creature in self.pop:
			if creature.fitness < -200:
				self.refill()
				self.pop.remove(creature)
			nval = self.get_nearest(creature)
			if creature.position[0] >= nval.position[0] >= creature.position[0] - 10 or creature.position[0] <= nval.position[0] <= creature.position[0] + 10:
				if creature.position[1] >= nval.position[1] >= creature.position[1] - 10 or creature.position[1] <= nval.position[1] <= creature.position[1] + 10:
					self.refill()
					self.refill()
					self.pop.remove(creature)
					self.pop.remove(nval)
	def get_best(self):
		chosen = random.random()*sum([x.fitness for x in self.pop])
		total = 0
		for creature in self.pop:
			total += creature.fitness
			if total >= chosen:
				return creature
		return self.get_oblg_best()
	def get_oblg_best(self):
		best = random.sample(self.pop,1)[0]
		ft_best = 0
		for creature in self.pop:
			if ft_best <= creature.fitness:
				best = creature
				ft_best = creature.fitness
		return best
	def refill(self):
		old = self.get_best()
		new = evo_c.Creature(old.data[0],old.data[1])
		new.brain.layers = old.brain.copy()
		new.brain.learn(50,0,10)
		self.pop.append(new)

display = evo_g.Renderer((800,800))
test = Enviroment(display)
for x in range(50):
	test.populate(evo_c.Creature([4,6,5,4],initial=True))

epsilon  = 50
a = test.pop[0]
while True:
	test.check_for_deaths()
	for bob in test.pop:
		if False: #random.randint(0,epsilon) == epsilon:
			bob.move(random.randint(0,3))
		else:
			near = test.get_nearest(bob).position
			r = bob.brain.think([bob.position[0],bob.position[1],near[0],near[1]])
			chosen = r.index(max(r))
			bob.move(chosen)
	test.update_all()
	display.update()