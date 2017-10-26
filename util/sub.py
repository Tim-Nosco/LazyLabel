from instr import Instruction

class Sub(Instruction):
	regx = Instruction.regx.format("sub")
	def execute(self):
		return [self.result==(self.arg1-self.arg2)]