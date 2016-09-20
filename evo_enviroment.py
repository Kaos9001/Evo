import evo_graphic as evo_g
import evo_creature as evo_c
import random

class Food:
	def __init__(self,enviroment):
		self.enviroment = enviroment
		self.position = (random.randint(0,enviroment.renderer.size[0]),random.randint(0,enviroment.renderer.size[1]))
		self.fitness = 1000
		self.SIZE = 20
	def draw(self):
		self.SIZE = int(self.fitness/50.0)+5
		self.enviroment.renderer.draw_dot(self.position,self.SIZE,(220,110,180))
		self.enviroment.renderer.draw_dot(self.position,max(0,self.SIZE-8),(50,50,50))


class Better:
	def __init__(self,renderer):
		self.pop = {}
		self.food = []
		self.types = {}
		self.renderer = renderer
		self.odd_food = 100
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
		for food in self.food:
			food.draw()
			if food.fitness < 0:
				self.food.remove(food)
				self.odd_food /= 1.5
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
		new.color = tuple([max(0, min(220, x+random.randint(-20,20))) for x in old.color])
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
	def get_nearest_food(self,creature):
		point = creature.position
		best = None
		smallest = 999999
		for other in self.food:
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
	def check_food_collisions(self):
		for ctype in self.pop:
			for creature in self.pop[ctype]:
				for food in self.food:
					if creature.position[0] >= food.position[0] >= creature.position[0] - (creature.SIZE+food.SIZE) or creature.position[0] <= food.position[0] <= creature.position[0] + (creature.SIZE+food.SIZE):
						if creature.position[1] >= food.position[1] >= creature.position[1] - (creature.SIZE+food.SIZE) or creature.position[1] <= food.position[1] <= creature.position[1] + (creature.SIZE+food.SIZE):
							creature.food_collision_hook()
							food.fitness -= 5
	def spawn_food(self):
		if random.randint(0,int(self.odd_food)) == int(self.odd_food):
			self.food.append(Food(self))
			self.odd_food *= 1.5
	def update_self(self):
		test.spawn_food()
		test.check_collisions()
		test.check_food_collisions()

display = evo_g.Renderer((1000,1000))
test = Better(display)
test.populate([(evo_c.Ballie,50,[6,6,5,4])])

epsilon  = 10
while True:
	test.update_self()
	for ctype in test.pop:
		for bob in test.pop[ctype]:
			if False: #random.randint(0,epsilon) == epsilon:
				bob.move(random.randint(0,3))
			else:
				#near = test.get_nearest(bob).position
				food = test.get_nearest_food(bob)
				if food == None:
					food = (-1,-1)
				else:
					food = food.position
				r = bob.brain.process([bob.position[0],bob.position[1],food[0],food[1]])
				chosen = r.index(max(r))
				bob.move(chosen)
	test.update_all()
	display.update()