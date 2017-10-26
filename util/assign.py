from instr import Instruction

class Assign(Instruction):
	regx = r"^{0} = {0} (\d+)$".format(Instruction.valid_names)
	def __init__(self,idx,result,rtype,arg1):
		self.result = result
		self.type = rtype
		self.arg1 = int(arg1)
	def unknown_vars(self):
		return []
	def fill_unknown_vars(self,*args):
		pass
	def execute(self):
		return [self.result==self.arg1]