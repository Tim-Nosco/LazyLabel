from instr import Instruction
from z3 import *

class Icmp(Instruction):
	regx = "^{0} = icmp {0} {0} {0}, {0}$".format(Instruction.valid_names)
	def __init__(self,idx,result,cond,rtype,arg1,arg2):
		self.result = result
		self.cond_code = cond
		self.type = rtype
		self.arg1 = arg1
		self.arg2 = arg2
	def setup(self):
		self.convert_type()
		#TODO: interpret self.cond_code
		if self.cond_code == "eq":
			self.op = lambda x,y: x==y
		elif self.cond_code == "ne":
			self.op = lambda x,y: x!=y
		elif self.cond_code == "ugt":
			self.op = lambda x,y: x>y
		elif self.cond_code == "uge":
			self.op = lambda x,y: x>=y
		elif self.cond_code == "ult":
			self.op = lambda x,y: x<y
		elif self.cond_code == "ule":
			self.op = lambda x,y: x<=y
	def create_result_vec(self):
		tmp = self.result
		self.result = Bool(tmp)
		return (tmp,self.result)
	def execute(self):
		return [self.result == self.op(self.arg1,self.arg2)]