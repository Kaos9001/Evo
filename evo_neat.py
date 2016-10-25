import random
import scipy.special as sp
import keypair as kp

parser = kp.Parser(open("evo_metadata.kp"))
parser.parse(type_result=float)
innovation = 0
mutations = []

class Mut:
	def __init__(self,name,_in=None,out=None,oldcon=None):
		self._in = _in
		self.out = out
		self.oldcon = oldcon
		self.name = name


class Basic:
	def metadata(self,key):
		try:
			return parser.get_bracket_dict(self.__class__.__name__)[key]
		except:
			raise(KeyError("Class '" + self.__class__.__name__ + "' doesn't have key value '" + key + "'"))


class Population(Basic):
	def __init__(self,fitness_func,pop_size):
		self.pop = [] # List of Species
		self.fitcheck = fitness_func
		self.pop_size = pop_size
		self.best = None
		self.specie_n = 0
	def get_all(self):
		all = []
		for species in self.pop:
			new += species.get_members()
		return all
	def crossover(self,gene_1,gene_2):
		new = {}
		if gene_1.fitness > gene_2.fitness:
			net_best = gene_1.network.get_dict()
			net_worst = gene_2.network.get_dict()
		else:
			net_best = gene_2.network.get_dict()
			net_worst = gene_1.network.get_dict()
		for innov in net_best.keys():
			if innov in net_worst.keys():
				if random.random() < self.metadata("strong_parent_passdown_chance"):
					new[innov] = net_best[innov].copy()
				else:
					new[innov] = net_worst[innov].copy()
			else:
				new[innov] = net_best[innov].copy()
		for innov in net_worst.keys():
			if innov not in net_best.keys() and random.random() > self.metadata("worst_pass_chance"):
				new[innov] = net_worst[innov].copy()
		net = Network(len(gene_1.network.inputs),len(gene_1.network.outputs))
		for innov in new.keys():
			if new[innov].__class__.__name__ == 'Node':
				#print("Passing node " + str(innov))
				cons_out_new = []
				for connection in new[innov].connections_out:
					try:
						cons_out_new.append(new[connection])
					except:
						pass
				new[innov].connections_out = cons_out_new[:]
				cons_in_new = []
				for connection in new[innov].connections_in:
					if connection in new.keys():
						cons_in_new.append(new[connection])
				new[innov].connections_in = cons_in_new
				net.nodes.append(new[innov])
			elif new[innov].__class__.__name__ == "Connection":
				if new[innov]._in in new.keys() and new[innov].out in new.keys():
					new[innov]._in = new[new[innov]._in]
					new[innov].out = new[new[innov].out]
					net.nodes.append(new[innov])
			else:
				print("What")
		final = Genome()
		final.network = net
		return final
	def add_new(self,creature):
		for specie in self.pop:
			if specie.test_add(creature):
				break
		else:
			s = Species(self.specie_n)
			self.specie_n += 1
			s.get_members().append(creature)
			self.pop.append(s)
			print("New species " + str(self.specie_n))
			s.rep = creature
	def add_n_basic(self,amount,input_shape,output_shape):
		#self.pop.append(Species(self.specie_n))
		#self.specie_n += 1
		for n in range(amount):
			new = Genome()
			new.make_minimal_network(input_shape,output_shape)
			new.mutate()
			self.add_new(new)
			#self.pop[len(self.pop)-1].members.append(new)
	def rate_all(self):
		for specie in self.pop:
			for creature in specie.get_members():
				creature.fitness = specie.get_fitness(self.fitcheck(creature))
				try:
					if creature.fitness > self.best.fitness:
						self.best = creature
				except:
					self.best = creature
	def purge_weak(self):
		min_fit = self.metadata("min_fitness")
		for specie in self.pop:
			for creature in specie.get_members():
				if creature.fitness < min_fit:
					specie.members.remove(creature)
	def clean(self):
		for specie in self.pop:
			specie.members = []
	def check(self):
		new = self.pop[:]
		for specie in self.pop:
			#print(str(specie.ID) + ": " + str(len(specie.members)) + ": " + str(specie.members))
			if len(specie.members) == 0:
				specie.grace += 1
				if specie.grace > self.metadata("specie_grace_period"):
					print("Specie " + str(specie.ID) + " died out")
					new.remove(specie)
			else:
				specie.grace = 0
		self.pop = new
	def loop(self):
		self.rate_all()
		#self.purge_weak()
		for x in self.pop:
			#print(str(x.ID)+ ": " + str(x.members))
			x.rank()
		new = []
		for _ in range(self.pop_size):
			specie = self.choose_specie()
			one = specie.get_ranked()
			two = one
			while two == one and len(specie.members) > 1:
				two = specie.get_ranked()
			c = self.crossover(one,two)
			c.mutate()
			new.append(c)
			odds = self.metadata("more_son_odds")
			while random.random() < odds:
				c = self.crossover(one,two)
				c.mutate()
				new.append(c)
				odds /= self.metadata("diminishing")
		self.clean()
		for creature in new:
			self.add_new(creature)
		self.check()
	def choose_specie(self):
		return random.sample(self.pop,1)[0]

class Species(Basic):
	def __init__(self,ID):
		self.ID = ID
		self.members = []
		self.grace = 0
		self.color = (random.randint(30,255),random.randint(30,255),random.randint(30,255))
		self.rep = None
	def get_rep(self):
		return self.rep
	def get_members(self):
		return self.members
	def rank(self):
		if self.grace == 0:
			self.members.sort()
			self.members.reverse()
			for ind, fit in enumerate(self.members):
				fit.odds = 1/(2+ind)
	def get_ranked(self):
		chosen = random.uniform(0,sum([x.odds for x in self.members]))
		total = 0
		for x in self.members:
			total += x.odds
			if total > chosen:
				return x
		return self.rep
	def get_compatibility(self,other):
		dist = 0.0
		rep = self.get_rep().network.get_dict()
		other = other.network.get_dict()
		if len(rep) > len(other):
			larger = len(rep)
		else:
			larger = len(other) 
		if larger == 0:
			larger = 1
		diff = set(rep.keys()).symmetric_difference(set(other.keys()))
		same = set(rep.keys()).intersection(set(other.keys()))
		dist += len(diff) * self.metadata("structure_distance_mult") / larger
		same = [[rep[x],other[x]] for x in same if rep[x].__class__.__name__ == "Connection"]
		for connections in same:
			dist += abs(float(connections[0].weight) - float(connections[1].weight)) * self.metadata("weight_distance_mult")
		return dist
	def test_add(self,other):
		if self.get_compatibility(other) < self.metadata("minimum_compatibility"):
			self.members.append(other)
			return True
		return False
	def get_fitness(self,fitness):
		return fitness / len(self.members)
	def kill(self,genome):
		if genome in self.members:
			self.members.remove(genome)


class Genome(Basic):
	def __init__(self):
		self.network = None
		self.fitness = 0
		self.odds = None
	def make_minimal_network(self,input_shape,output_shape):
		new = Network(input_shape,output_shape)
		new.connect_basic()
		self.network = new
	def mutate(self):
		if random.random() < self.metadata("mutate_add_node_odds"):
			self.network.mutate_add_node()
		if random.random() < self.metadata("mutate_remove_node_odds"):
			self.network.mutate_remove_node()
		val = random.random()
		if val < self.metadata("mutate_add_connection_odds"):
			#print(str(self.metadata("mutate_add_connection_odds")) + " vs " + str(val))
			self.network.mutate_add_conn()
		if random.random() < self.metadata("mutate_remove_connection_odds"):
			self.network.mutate_remove_conn()
		self.network.mutate_weights(self.metadata("mutate_weight_odds"))
		self.network.mutate_biases(self.metadata("mutate_bias_odds"))
	def __lt__(self,other):
		if other.fitness > self.fitness:
			return other
		else:
			return self

class Network(Basic):
	def __init__(self,inputs_amount,outputs_amount):
		self.nodes = []
		self.inputs = [Input() for _ in range(inputs_amount)]
		self.outputs = [Node(-1) for _ in range(outputs_amount)]
		self.connections = []
	def get_dict(self):
		return {char.id:char for char in self.nodes+self.connections}
	def run(self,inputs):
		for ind, node in enumerate(self.inputs):
			node.set_value(inputs[ind])
			for connection in node.connections_out:
				connection.run()
		self.reset_state()
		return [node.fire() for node in self.outputs]
	def reset_state(self):
		for node in self.nodes + self.outputs:
			node.fired = 0
		for connection in self.connections:
			connection.has_run = False
	def mutate_weights(self,odds):
		for conn in self.connections:
			if random.random() < odds:
				conn.mutate_weight()
	def mutate_biases(self,odds):
		for node in self.nodes+self.outputs:
			if node.__class__ == Connection:
				print("why")
			if random.random() < odds:
				node.mutate_bias()
	def mutate_add_node(self):
		if len(self.connections) > 0:
			global innovation
			global mutations
			old_con = random.sample(self.connections,1)[0]
			for mut in mutations:
				if mut.name == "Node":
					if mut.oldcon == old_con.id:
						return
			innovation += 1
			new_node = Node(innovation)
			print("Adding node " + str(innovation) + " to conn " + str(old_con.id))
			old_node = old_con.out
			old_con.set_nodes(old_con._in,new_node)
			innovation += 1
			new_con = Connection(innovation)
			new_con.set_nodes(new_node,old_node)
			self.connections.append(new_con)
			self.nodes.append(new_node)
			mutations.append(Mut("Node",oldcon=old_con.id))
	def mutate_add_conn(self):
		node_1 = random.sample(self.nodes+self.inputs,1)[0]
		node_2 = random.sample(self.nodes+self.outputs,1)[0]
		for conn in self.connections:
			if (conn._in == node_2 and conn.out == node_1) or (node_1 == node_2):
				return
		for mut in mutations:
				if mut.name == "Connection":
					if mut._in == node_2.id and mut.out == node_1.id:
						return
		global innovation
		innovation += 1
		print("Adding conn " + str(innovation))
		new_con = Connection(innovation)
		new_con.set_nodes(node_2,node_1)
		self.connections.append(new_con)
		mutations.append(Mut("Connection",_in=node_2.id,out=node_1.id))
	def mutate_remove_conn(self):
		if len(self.connections) > 2:
			con = random.sample(self.connections,1)[0]
			con.clean()
			self.connections.remove(con)
	def mutate_remove_node(self):
		if len(self.nodes) > 0:
			node = random.sample(self.nodes,1)[0]
			for connection in node.connections_out+node.connections_in:
				connection.clean()
				self.connections.remove(connection)
			self.nodes.remove(node)
	def connect_basic(self):
		x = 0
		for node in self.inputs:
			for node_out in self.outputs:
				x += 1
				con = Connection(x)
				con.set_weight(1)
				con.set_nodes(node_out,node)
				self.connections.append(con)

class Node(Basic):
	def __init__(self,id):
		self.id = id
		self.bias = 0
		self.value = 0
		self.connections_out = []
		self.connections_in = []
		self.fired = 0
	def add_connection_out(self,connection):
		self.connections_out.append(connection)
	def add_connection_in(self,connection):
		self.connections_in.append(connection)
	def remove_connection_out(self,connection):
		assert connection in self.connections_out
		self.connections_out.remove(connection)
	def remove_connection_in(self,connection):
		assert connection in self.connections_in
		self.connections_in.remove(connection)
	def set_bias(self,new_bias):
		self.bias = new_bias
	def mutate_bias(self):
		mut_total_chance = self.metadata("mut_total_chance")
		if random.random() < mut_total_chance:
			new_value_range = self.metadata("mut_total_new")
			self.bias = random.uniform(-new_value_range,new_value_range)
		else:
			mut_size = self.metadata("mut_size")
			self.bias += random.uniform(-mut_size,mut_size)
	def get_layer(self):
		if self.__class__.__name__ == "Input":
			return 1
		layers = []
		for con in self.connections_in:
			layers.append(1 + con._out.get_layer())
		return max(layers)
	def fire(self):
		if self.fired < len(self.connections_in):
			for connection in self.connections_in:
				connection.run()
		return sp.expit(self.value + self.bias)
	def receive(self,value):
		self.fired += 1
		self.value += value
		#self.fire()
	def copy(self):
		new =Node(self.id)
		new.bias = self.bias
		new.connections_out = [con.id for con in self.connections_out]
		new.connections_in = [con.id for con in self.connections_in]
		return new

class Input(Node):
	def __init__(self):
		self.id = -2
		self.connections_out = []
		self.value = 0
	def set_value(self,value):
		self.value = value
	def fire(self):
		return self.value

class Connection(Basic):
	def __init__(self,id):
		self.id = id
		self.has_run = False
		self._in = None
		self.out = None
		self.weight = 1
	def set_nodes(self,_in,out):
		self._in = _in
		self._in.add_connection_in(self)
		self.out = out
		self.out.add_connection_out(self)
	def clean(self):
		self._in.remove_connection_in(self)
		self.out.remove_connection_out(self)
	def set_weight(self,new_weight):
		self.weight = new_weight
	def mutate_weight(self):
		mut_total_chance = self.metadata("mut_total_chance")
		if random.random() < mut_total_chance:
			new_value_range = self.metadata("mut_total_new")
			self.weight = random.uniform(-new_value_range,new_value_range)
		else:
			mut_size = self.metadata("mut_size")
			self.weight += random.uniform(-mut_size,mut_size)
	def run(self):
		if not self.has_run:
			new = self.out.fire()
			self._in.receive(new)
			#print("Con " + str(self.id) + " has fired " + str(new) + " from " + str(self.out.id) + " to " + str(self._in.id) + "; new value: " + str(self._in.value))
			self.has_run = True
	def copy(self):
		new = Connection(self.id)
		new.weight = self.weight
		new._in = self._in.id
		new.out = self.out.id
		return new


def xor(a,b):
	return int((a and not b) or (b and not a))

def fit(creature):
	return len(creature.network.nodes)


def good_fit(creature):
	errors = []
	for x in range(50):
		inputs = [random.randint(0,1),random.randint(0,1)]
		right = xor(*inputs)
		out = creature.network.run(inputs)
		errors.append(4-pow((abs(right - out[0])),2))
	return sum(errors)/len(errors)

pop = Population(good_fit,100)
pop.add_n_basic(100,2,1)
for x in range(150):
	if pop.best != None:
		print(pop.best.network.get_dict())
		print("Current species are: ")
		for specie in pop.pop:
			print("\tSpecie " + str(specie.ID) + ": " + str(len(specie.members)) + " members with rep: " + str(specie.rep.network.get_dict()))
	pop.loop()

print(pop.best.fitness)
