from z3 import *
import logging

class Labeler:
	def __init__(self,n):
		logging.debug("Setting up labeler")
		self.n = n
		logging.debug("Creating edges and verticies")
		self.edges = []
		self.vert = []
		self.clauses = []
		for i in range(n+1):
			v = Int("v{}".format(i))
			self.vert.append(v)
			self.clauses.append(v >= 0)
			self.clauses.append(v <= n)
		for i in range(n):
			e = Int("e{}".format(i))
			self.edges.append(e)
			self.clauses.append(e >= 1)
			self.clauses.append(e <= n)
		self.clauses += [Distinct(*self.edges),
						 Distinct(*self.vert)]
		self.setup()
	def setup(self):
		self.s.reset()
		self.s.insert(*self.clauses)
	def reject(self):
		logging.debug("Checking with solver...")
		r = s.check()
		logging.debug("Solver: {}",r)
		return r==sat
	def connect(self):
		#TODO assert that an edge is the connection of two verticies
		# hope that the solver returns unsat (a labeling does not exist)
		pass