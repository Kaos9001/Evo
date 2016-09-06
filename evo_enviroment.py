import evo_graphic as evo_g
import evo_creature as evo_c
import random

class Enviroment:
	def __init__(self,renderer):
		self.renderer = renderer
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
		best = [None,None]
		smallest = 999999
		for other in self.pop:
			if other != creature:
				num = (creature.position[0]-other.position[0])**2+(creature.position[1]-other.position[1])**2
				if num < smallest:
					smallest = num
					best = other.position
		return best
	def check_for_deaths(self):
		i = 0
		for creature in self.pop:
			for num, item in enumerate(creature.position):
				if item > 800 or item < 0:
					try:
						self.pop.remove(creature)
					except:
						print("SHSSHHH")
					i += 1
		for  _ in range(i):
			self.refill()
	def get_best(self):
		best = 0
		new = None
		for creature in self.pop:
			if creature.fitness > best:
				best = creature.fitness
				new = creature
		return creature
	def refill(self):
		old = self.get_best()
		new = evo_c.Creature(old.data[0],old.data[1])
		new.brain.layers = old.brain.copy()
		self.pop.append(new)

display = evo_g.Renderer((800,800))
test = Enviroment(display)
for x in range(50):
	test.populate(evo_c.Creature([4,6,4],initial=True))

i  = 42
a = test.pop[0]
while True:
	test.check_for_deaths()
	for bob in test.pop:
		bob.brain.learn(10,0,0.2)
		if random.randint(0,i) == i:
			bob.move(random.randint(0,3))
		else:
			r = bob.brain.think([bob.position[0],bob.position[1],bob.velocity[0],bob.velocity[1]])
			chosen = r.index(max(r))
		bob.move(chosen)
	test.update_all()
	display.update()