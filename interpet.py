import re, logging
from instructions import by_name

class Parser:
	def __init__(self,filename=None,lines=None):
		assert(bool(filename) or bool(lines))
		if filename:
			with open(filename,'r') as f:
				lines = f.read()
		self.data = lines
		#remove comments, replace newlines with semicolins
		data = re.sub("(?:;.*)?\n",";",self.data)
		#regex for instruction parsing
		#instructions must be of the format:
		# <RESULT> = <INST> <TYPE> <ARG1>, <ARG2>
		#<INST> may have spaces in it, such as: "add nsw"
		regx = re.compile(r"^\s*(.+?) = (.+) (.+?) (.+?), (.+?)\s*$")
		self.program = []
		for instr, line in enumerate(re.split(r';',data)):
			m = re.match(regx,line)
			if m:
				groups = m.groups()
				instr_name = groups[1]
				args = groups[:1]+groups[2:]
				#lookup instr based on instr_name
				instr = by_name[instr_name]
				logging.debug("Found instruction %s, args:%s", instr_name, args)
				self.program.append(instr(*args))
			elif line:
				logging.error("PARSING FAILED ON INSTRUCTION: %s\n%s", instr,line)
				raise Exception("Failed to parse input file.")
def usage():
	#TODO
	pass
if __name__=="__main__":
	import sys
	logging.basicConfig(level=logging.DEBUG)
	if len(sys.argv): #TODO make > 1
		test = "<result> = add i32 4, %var          ; yields i32:result = 4 + %var\n"
		p = Parser(lines=test)
	else:
		usage()