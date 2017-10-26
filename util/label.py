import re
from instr import Instruction
class Label(Instruction):
	regx = re.compile(r"^{0}:$".format(Instruction.valid_names))
	def __init__(self,idx,name):
		self.idx = idx
		self.name = name
	def setup(self):
		pass
	def get_new_vars(self):
		return [(self.name,self)]
	def unknown_vars(self):
		return []
	def fill_unknown_vars(self,*args):
		pass
	def execute(self):
		return []