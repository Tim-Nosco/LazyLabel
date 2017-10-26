from instr import Instruction

class Add(Instruction):
	regx = Instruction.regx.format("add")
	def execute(self):
		return [self.result == (self.arg1+self.arg2)]