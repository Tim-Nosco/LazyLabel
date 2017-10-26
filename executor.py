import logging
from z3 import *

class Executor:
	def __init__(self,program):
		self.program = program
		self.s = Solver()

	def run_instr(self,instr,branch_constraints,*args):
		constraints = instr.execute(*args)
		for c in constraints:
			branch_constraints.append(c)
		self.s.insert(*constraints)
		return instr.next_instr
	def start(self, instr):
		branch_constraints = []
		while instr:
			logging.debug("Executing: %s",instr)
			if instr.__class__.__name__=="Br":
				logging.debug("Found branch, taking True path...")
				#save the solver's state
				self.s.push()
				#run the true branch to return
				tmp = self.run_instr(instr,[],True)
				true_constraints = self.start(tmp)
				#restore the solver's state,
				#run false branch to return
				self.s.pop()
				logging.debug("Returned from recurse, taking False path...")
				self.s.push()
				tmp = self.run_instr(instr,[],False)
				false_constraints = self.start(tmp)
				self.s.pop()
				#merge the true and false constraints
				logging.debug("True constraints: %s", true_constraints)
				logging.debug("False constraints: %s", false_constraints)
				self.s.insert(true_constraints[:-1])
				branch_constraints+= true_constraints
				self.s.insert(false_constraints[:-1])
				branch_constraints+= false_constraints
				ite = If(instr.cond,true_constraints[-1],false_constraints[-1])
				self.s.add(ite)
				branch_constraints.append(ite)
				logging.debug("Final path model: %s",self.s)
				return branch_constraints
			else:	
				instr = self.run_instr(instr,branch_constraints)
		logging.debug("Final path model: %s",self.s)
		return branch_constraints