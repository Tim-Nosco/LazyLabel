from instr import Instruction

class Ret(Instruction):
	regx = "^ret {0} {0}$".format(Instruction.valid_names)
	def __init__(self,idx,rtype,value):
		self.type = rtype
		self.arg1 = value
	def setup(self):
		Instruction.setup(self)
		self.next_instr = None
	def get_new_vars(self):
		return []
	def unknown_vars(self):
		return (self.arg1,"RETURN")
	def fill_unknown_vars(self,*args):
		self.arg1 = args[0]
		self.return_vec = args[1]
	def create_result_vec(self):
		pass
	def execute(self):
		return [self.return_vec == self.arg1]