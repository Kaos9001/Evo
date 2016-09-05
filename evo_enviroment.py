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
		self.renderer.draw_dot(creature.position,10,(255,0,0))
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

display = evo_g.Renderer((800,800))
test = Enviroment(display)
for x in range(50):
	test.populate(evo_c.Creature([2,5,4],initial=True))

i  = 42
a = test.pop[0]
while True:
	for bob in test.pop:
		bob.brain.learn(0.05)
		r = bob.brain.think(bob.position)
		chosen = r.index(max(r))
		if bob == a:
			print(r)
			print(chosen)
		bob.move(chosen)
	test.update_all()
	display.update()
