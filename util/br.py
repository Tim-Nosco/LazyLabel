import re
from instr import Instruction
from z3 import *

class Br(Instruction):
	regx = re.compile(r"^br i1 {0}, label %?{0}, label %?{0}$".format(Instruction.valid_names))
	def __init__(self,idx,conditional,label_true,label_false):
		self.cond = conditional
		self.iftrue = label_true
		self.iffalse = label_false
		self.type = 1
	def setup(self):
		pass
	def get_new_vars(self):
		return []
	def unknown_vars(self):
		return self.iftrue, self.iffalse, self.cond
	def fill_unknown_vars(self,*args):
		self.iftrue = args[0]
		self.iffalse = args[1]
		self.cond = args[2]
		#TODO fix self.next_instr
		self.next_instr = self.iftrue
	def execute(self,cond=True):
		self.next_instr = self.iftrue if cond else self.iffalse
		return [self.cond==cond]