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


display = evo_g.Renderer((800,800))
test = Enviroment(display)
for x in range(100):
	test.populate(evo_c.Creature())

i  = 42
while True:
	for bob in test.pop:
		num = random.randint(0,3)
		bob.move(num)
	test.update_all()
	display.update()
