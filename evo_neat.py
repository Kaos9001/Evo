import random
import scipy.special as sp
import keypair as kp

parser = kp.Parser(open("evo_metadata.kp"))
parser.parse(type_result=float)
innovation = 0

class Basic:
	def metadata(self,key):
		try:
			return parser.get_bracket_dict(self.__class__.__name__)[key]
		except:
			raise(KeyError("Class '" + self.__class__.__name__ + "' doesn't have key value '" + key + "'"))


class Population(Basic):
	def __init__(self):
		self.pop = [] # List of Species
	def get_all(self):
		all = []
		for species in self.pop:
			new += species.get_members()
		return all

class Species(Basic):
	def __init__(self,ID):
		self.ID = ID
		self.members = []
		self.color = (random.randint(30,255),random.randint(30,255),random.randint(30,255))
	def get_rep(self):
		return self.members[0]
	def get_members(self):
		return members

class Genome(Basic):
	def __init__(self):
		self.networks = []
		self.fitness = None
	def make_minimal_network(self,input_shape,output_shape):
		new = Network()
		in_nodes = []
		out_nodes = []
		for node in range(input_shape):
			pass

class Network(Basic):
	def __init__(self,inputs_amount,outputs_amount):
		self.nodes = []
		self.inputs = [Input() for _ in range(inputs_amount)]
		self.outputs = [Node(-1) for _ in range(outputs_amount)]
		self.connections = []
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
	def connect_basic(self):
		for node in self.inputs:
			for node_out in self.outputs:
				con = Connection(-1)
				con.set_weight(1)
				con.set_nodes(node_out,node)

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
	def set_bias(self,new_bias):
		self.bias = new_bias
	def mutate_bias(self):
		mut_total_chance = self.metadata("mut_total_chance")
		if random.random < mut_total_chance:
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
	def set_weight(self,new_weight):
		self.weight = new_weight
	def mutate_weight(self):
		mut_total_chance = self.metadata("mut_total_chance")
		if random.random < mut_total_chance:
			new_value_range = self.metadata("mut_total_new")
			self.weight = random.uniform(-new_value_range,new_value_range)
		else:
			mut_size = self.metadata("mut_size")
			self.weight += random.uniform(-mut_size,mut_size)
	def run(self):
		if not self.has_run:
			new = self.out.fire()
			self._in.receive(new)
			print("Con " + str(self.id) + " has fired " + str(new) + " from " + str(self.out.id) + " to " + str(self._in.id) + "; new value: " + str(self._in.value))
			self.has_run = True