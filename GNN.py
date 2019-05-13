import math
import random
from threading import Thread
from copy import deepcopy
from standard_settings import get_standard_settings

#random.randrange(a, b) a <= N < b
#random.uniforn(a, b) a <= N <= b

class Genome:
	def __init__(self, u_id, dimentions, input_size, output_size, alowed_activation, settings):
		self.id = u_id								#int of uniqe id
		self.dimentions = dimentions				#tuple of dimentions (layers, space per layer)
		self.input_size = input_size				#int of input size
		self.output_size = output_size				#int of output size
		self.alowed_activation = alowed_activation	#list of activationfunctions
		self.settings = settings					#dict of settings

		#Create a bace network

		self.space = []
		self.space.append([None] * self.input_size)
		for x in range(self.input_size):
			self.space[0][x] = self.In(0)
		
		for x in range(self.dimentions[0]):
			self.space.append([None] * self.dimentions[1])
		self.space.append([None] * self.output_size)
		
		poss = [random.randrange(0, self.dimentions[0]) + 1, random.randrange(0, self.dimentions[1])]
		self.space[poss[0]][poss[1]] = self.Gene(self.output_size, (poss[0], poss[1]), {}, random.choice(self.alowed_activation))
		
		fail = True
		for x in range(self.input_size):
			if random.random() < 0.5:
				self.space[poss[0]][poss[1]].con[self.space[0][x]] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])
				fail = False
		if fail:
			self.space[poss[0]][poss[1]].con[self.space[0][random.randrange(0, self.input_size)]] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])
		
		for x in range(self.output_size):
			self.space[-1][x] = self.Gene(x, (self.dimentions[0] + 1, x), {}, random.choice(self.alowed_activation))
			fail = True
			for o in self.lower_objects(self.space[-1][x].poss[0]):
				if random.random() < 0.5:
					self.space[-1][x].con[o] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])
					fail = False
			if fail:
				self.space[-1][x].con[random.choice(self.lower_objects(self.space[-1][x].poss[0]))] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])

		lose = True
		for x in range(self.output_size):
			if self.space[poss[0]][poss[1]] in self.space[-1][x].con:
				lose = False
				break
		if lose:
			self.space[poss[0]][poss[1]] = None

	def del_lose_genes(self):
		for x in list(set(self.higher_objects(0)) - set(self.space[-1])):
			lose = True
			for o in self.higher_objects(x.poss[0]):
				if x in o.con:
					lose = False
					break
			if lose:
				self.space[x.poss[0]][x.poss[1]] = None
		
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
		for x in range(self.dimentions[0]):
			for y in range(self.dimentions[1]):
				if self.space[1 + x][y] == None:
					out.append((1 + x, y))
		return out

	def count_genes(self):
		out = 0
		for x in range(self.dimentions[0]):
			for y in range(self.dimentions[1]):
				if self.space[1 + x][y] != None:
					out += 1
		if out == 0:
			for x in range(self.output_size):
				if self.space[-1][x] != None:
					out += 1
		else:
			out += self.output_size
		return out
	
	def mutate(self):
		if random.random() < self.settings["node_add_rate"]:
			try:
				poss = random.choice(self.free_space())
				self.space[poss[0]][poss[1]] = self.Gene(self.count_genes(), (poss[0], poss[1]), {}, random.choice(self.alowed_activation))
				self.space[poss[0]][poss[1]].con[random.choice(self.lower_objects(poss[0]))] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])
				random.choice(self.higher_objects(poss[0])).con[self.space[poss[0]][poss[1]]] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])
			except:
				pass

		if random.random() < self.settings["node_remove_rate"]:
			nodes = list(set(self.higher_objects(0)).intersection(set(self.lower_objects(-1))))
			if nodes != None:
				node = random.choice(nodes)
				poss = node.poss
				for x in self.higher_objects(poss[0]):
					if node in x.con:
						del x.con[node]
				self.space[poss[0]][poss[1]] = None

		if random.random() < self.settings["connection_add_rate"]:
			gens = self.higher_objects(0)
			random.shuffle(gens)
			done = False
			for o in gens:
				pcons = self.lower_objects(o.poss[0])
				random.shuffle(pcons)
				for c in pcons:
					if c not in o.con:
						o.con[c] = random.uniform(self.settings["new_weight_min"], self.settings["new_weight_max"])
						done = True
						break
				if done:
					break

		if random.random() < self.settings["weight_change_rate"]:
			gens = self.higher_objects(0)
			random.shuffle(gens)
			done = False
			for o in gens:
				pcons = self.lower_objects(o.poss[0])
				random.shuffle(pcons)
				for c in pcons:
					if c in o.con:
						o.con[c] *= random.uniform(self.settings["weight_change_magnitude_min"], self.settings["weight_change_magnitude_max"])
						done = True
						break
				if done:
					break

		if random.random() < self.settings["activation_change_rate"]:
			gens = self.higher_objects(0)
			o = random.choice(gens)
			print(o)
			f = list(set(self.alowed_activation) - set([o.func]))
			if len(f) != 0:
				o.func = random.choice(f)
	
	def run(self, feed):
		if len(feed[0]) != self.input_size:
			raise ValueError("Lenght of feed: {0}, does not match the set input_size of: {1}".format(len(feed[0]), self.input_size))
		out = []
		for z in range(len(feed)):
			bit = []
			for y in range(self.input_size):
				self.space[0][y].val = feed[z][y]
			for x in range(self.output_size):
				bit.append(self.space[-1][x].run())
			out.append(bit)
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


class Population:
	def __init__(self, size, net_dimentions, input_size, output_size, alowed_activation, settings = get_standard_settings()):
		self.size = size
		self.settings = settings
		self.individuals = []
		self.net_dimentions = net_dimentions
		self.input_size = input_size
		self.output_size = output_size
		self.alowed_activation = alowed_activation
		for o in range(self.size):
			self.individuals.append(Genome(o, net_dimentions, input_size, output_size, alowed_activation, settings))
	
	def update_settings(self, settings):
		self.settings = settings
		for x in self.individuals:
			x.settings = settings

	def thread(self, thread_id, individuals, feed, results, fitt_func = None, y_ = None):
		if fitt_func != None:
			for x in range(len(individuals)):
				results[individuals[x].id] = fitt_func(individuals[x].run(feed), y_)
		else:
			for x in range(len(individuals)):
				results[individuals[x].id] = individuals[x].run(feed)

	def run(self, feed, fitt_func = None, y_ = None):
		threads = [None] * self.settings["computing_threads"]
		results = [None] * self.size
		if fitt_func != None:
			for i in range(len(threads)):
				threads[i] = Thread(target=self.thread, args=(i, self.individuals[i::self.settings["computing_threads"]], feed, results, fitt_func, y_))
				threads[i].start()
		else:
			for i in range(len(threads)):
				threads[i] = Thread(target=self.thread, args=(i, self.individuals[i::self.settings["computing_threads"]], feed, results))
				threads[i].start()
		for i in range(len(threads)):
			threads[i].join()
		return results

	def fitt(self, feed, fitt_func, y_ = None, return_best = False):
		results = self.run(feed, fitt_func = fitt_func, y_ = y_)
		best = deepcopy(self.individuals[results.index(max(results))])
		for x in range(self.size):
			self.individuals[x] = deepcopy(best)
			self.individuals[x].id = x

		for x in range(1, self.size):
			if x > self.size * self.settings["new_individual_rate"]:
				self.individuals[x].mutate()
			else:
				self.individuals[x] = Genome(x, self.net_dimentions, self.input_size, self.output_size, self.alowed_activation, self.settings)

		if return_best:
			return max(results)

	def get_fittest_individual(self, feed, fitt_func, y_ = None):
		results = self.run(feed, fitt_func = fitt_func, y_ = y_)
		best = deepcopy(self.individuals[results.index(max(results))])
		return best


class Activation:
	def sigmoid(x):
		try:
			sigm = 1. / (1. + math.exp(-x))
			return sigm
		except OverflowError:
			sigm = 1. / (1. + float("inf"))
			return sigm

	def relu(x):
		return x if x > 0 else 0

	def lrelu(x):
		return x if x > 0 else (0.01 * x)

	def tanh(x):
		return math.tanh(x)
