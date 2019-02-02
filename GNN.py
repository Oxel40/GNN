import math
import random
from copy import deepcopy

#random.randrange(a, b) a <= N < b
#random.uniforn(a, b) a <= N <= b
def get_standard_settings():
	out = {}
	out["node_add_rate"] = 0.2
	out["connection_add_rate"] = 0.3
	out["weight_change_rate"] = 0.8
	out["weight_change_magnitude_min"] = 0.8
	out["weight_change_magnitude_max"] = 1.2
	out["activation_change_rate"] = 0.
	#out[""] = 	
	return out


class Genome:
	def __init__(self, u_id, dimentions, input_size, output_size):
		self.id = u_id
		self.dimentions = dimentions
		self.input_size = input_size
		self.output_size = output_size

		self.space = []
		self.space.append([None] * self.input_size)
		for x in range(self.input_size):
			self.space[0][x] = self.In(0)
		
		for x in range(self.dimentions[1]):
			self.space.append([None] * self.dimentions[0])
		self.space.append([None] * self.output_size)
		
		poss = [random.randrange(0, self.dimentions[1]) + 1, random.randrange(0, self.dimentions[0])]
		self.space[poss[0]][poss[1]] = self.Gene(1, (poss[0], poss[1]), {}, Activation.sigmoid)
		
		fail = True
		for x in range(self.input_size):
			if random.random() < 0.5:
				self.space[poss[0]][poss[1]].con[self.space[0][x]] = random.uniform(-1, 1)
				fail = False
		
		if fail:
			self.space[poss[0]][poss[1]].con[self.space[0][random.randrange(0, self.input_size)]] = random.uniform(-6, 6)
		
		for x in range(self.output_size):
			self.space[-1][x] = self.Gene(0, (self.dimentions[1] + 1, x), {}, Activation.sigmoid)
			fail = True
			for o in self.lower_objects(self.space[-1][x].poss[0]):
				if random.random() < 0.5:
					self.space[-1][x].con[o] = random.uniform(-1, 1)
					fail = False
			
			if fail:
				self.space[-1][x].con[random.choice(self.lower_objects(self.space[-1][x].poss[0]))] = random.uniform(-6, 6)
					
	def lower_objects(self, layer):
		out = []
		for x in self.space[:layer]:
			for y in x:
				if y != None:
					out.append(y)
		return out
	
	
	def higher_objects(self, layer):
		out = []
		for x in self.space[layer + 1:]:
			for y in x:
				if y != None:
					out.append(y)
		return out
	
	
	def free_space(self):
		out = []
		for x in self.space:
			for y in x:
				if y == None:
					out.append(y)
		return out##########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	
	
	def mutate(self, settings):
		if random.random() < settings["node_add_rate"]:
			poss = [random.randrange(0, self.dimentions[1]) + 1, random.randrange(0, self.dimentions[0])]
			self.space[poss[0]][poss[1]] = self.Gene(1, (poss[0], poss[1]), {}, Activation.sigmoid)################!!!!!!!!!!!!!!!
	
	
	def run(self, feed):
		if len(feed) != self.input_size:
			raise ValueError("Lenght of feed: {0}, does not match the set input_size of: {1}".format(len(feed), self.input_size))
		for y in range(self.input_size):
			self.space[0][y].val = feed[y]
		out = []
		for x in range(self.output_size):
			out.append(self.space[-1][x].run())
		return out

	
	class In:
		def __init__(self, val):
			self.val = val
		
		def run(self):
			return self.val


	class Gene:
		def __init__(self, u_id, poss, con, func):
			self.id = u_id		#Uniqe id, int(id)
			self.poss = poss	#Possition, (x, y)
			self.con = con		#Connections, {object: weight}
			self.func = func	#Activation-function, func()
		
		def run(self):
			out = 0
			for x in self.con:
				out += x.run() * self.con[x]
			return self.func(out)
		

class Individual:
	def __init__(self, u_id, genes=[]):
		self.id = u_id
		self.genes = genes
	
	def run(self, data):
		pass


class Population:
	def __init__(self, size):
		self.size = size
	
	
class Activation:
	def sigmoid(x):
		sigm = 1. / (1. + math.exp(-x))
		return sigm






