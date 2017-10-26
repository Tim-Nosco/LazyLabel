import re,logging
from z3 import *

class Instruction:
	valid_names = r"([0-9A-z\%\<\>]+?)"
	regx = r"^{0} = {{}} {0} {0}, {0}$".format(valid_names)
	type_regx = re.compile(r"^i(\d+)$")
	def __init__(self,idx,result,rtype,arg1,arg2):
		self.result = result
		self.type = rtype
		self.arg1 = arg1
		self.arg2 = arg2
	def setup(self):
		self.convert_type()
	def get_new_vars(self):
		return [self.create_result_vec()]
	def unknown_vars(self):
		return self.arg1, self.arg2
	def fill_unknown_vars(self,*args):
		self.arg1 = args[0]
		self.arg2 = args[1]
	def create_result_vec(self):
		tmp = self.result
		self.result = BitVec(tmp,self.type)
		return (tmp,self.result)
	def convert_type(self):
		#determine type
		m = re.match(self.type_regx,self.type)
		if m:
			self.type = int(m.group(1))
		else:
			logging.error("Unable to interpret type: %s",self.type)
			raise Exception("Failed to parse instruction %s",self)
	def execute(self):
		logging.debug("Unimplemented execute: %s",self)
		return []
	def __repr__(self):
		return self.__class__.__name__