import re, logging
from instructions import as_list as instr_list
from z3 import *

class Parser:
	def __init__(self,filename=None,lines=None,debug=False):
		assert(bool(filename) or bool(lines))
		if filename:
			with open(filename,'r') as f:
				lines = f.read()
		self.data = lines
		#remove comments, replace newlines with semicolins
		data = re.sub("(?:;.*)?\n",";",self.data)
		self.program = []
		#add each instruction to self.program
		for instr, line in enumerate(re.split(r';',data)):
			line = line.strip()
			for i_type in instr_list:
				#find which instruction type matche
				m = re.match(i_type.regx,line)
				if m:
					args = m.groups()
					logging.debug("Found match %s, args:%s", i_type.__name__, args)
					self.program.append(i_type(instr,*args))
					if len(self.program)>1:
						#link each instruction to its next instruction
						#to increment program counter, we will call instr.next_instr
						self.program[-2].next_instr = self.program[-1]
					break
			else:
				#no instruction types matched
				if line:
					logging.error("PARSING FAILED ON INSTRUCTION: %s\n%s", instr,line)
					raise Exception("Failed to parse input file.")
		if not debug:
			all_vars = {"RETURN":BitVec("RETURN",32)}
			#first add all the result vectors (and labels) to the variable dict
			for instr in self.program:
				instr.setup()
				new_vars = instr.get_new_vars()
				for name,x in new_vars:
					logging.debug("ADDING VAR:%s -> %s",name,x)
					assert(name not in all_vars)
					all_vars[name]=x
			#next, look up variables to give to instructions (static single assignment)
			for instr in self.program:
				v = instr.unknown_vars()
				logging.debug("Looking for: %s -> %s",instr,v)
				v = map(lambda x: all_vars.get(x,BitVec(x,instr.type)),v)
				instr.fill_unknown_vars(*v)
def usage():
	print "TODO: USAGE"
	pass
if __name__=="__main__":
	import sys
	logging.basicConfig(level=logging.DEBUG)
	if len(sys.argv>1):
		p = Parser(sys.argv[1])
		#execute
	else:
		usage()