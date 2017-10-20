from z3 import *
import logging

def ABS_SUB(x,y):
	return If(x>y,x-y,y-x)

class Labeler:
	def __init__(self,tree):
		logging.debug("Setting up labeler")
		self.s = Solver()
		self.orig = tree
		self.n = len(tree)
		logging.debug("Creating edges and verticies")
		self.edges = []
		self.vert = []
		self.clauses = []
		for i in range(1,n+1):
			e = Int("e{}".format(i))
			self.edges.append(e)
			self.clauses.append(e >= 1)
			self.clauses.append(e <= n)
		for i in range(n+1):
			v = Int("v{}".format(i))
			self.vert.append(v)
			self.clauses.append(v >= 0)
			self.clauses.append(v <= n)
		self.clauses += [Distinct(*self.edges),
				Distinct(*self.vert)]
		self.setup()
	def setup(self):
		self.s.reset()
		self.s.insert(*self.clauses)
		#a label is an ordering of edge labels
		self.label = [i for i in range(1,n+1)]
	def assertLabel(self):
		for i,e in enumerate(self.label):
			v1,v2 = [self.vert[v] for v in self.orig[i]]
			edge = self.edges[e]
			self.s.add(edge==ABS_SUB(v1,v2))
	def reject(self):
		logging.debug("Checking with solver...")
		if not s.check():
			return True
		else:
			#TODO custom checks
			#if the check fails, append to self.clauses
			# set restart flag, return True
			return False
	


