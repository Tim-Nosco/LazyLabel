import unittest, logging
from parser import Parser
from executor import Executor

cond = """\
Test:
  %cond = icmp eq i32 %a, %b
  br i1 %cond, label %IfEqual, label %IfUnequal
IfEqual:
  %c = i32 1
  ret i32 %c
IfUnequal:
  %d = i32 0
  ret i32 %d
"""

cond2 = """\
%cond1 = icmp ugt i32 %a, %b
br i1 %cond1, label %0, label %1
0:
	%cond2 = icmp eq i32 %a, %b
	br i1 %cond2, label %2, label %3
	2:
		%c = sub i32 %a, %b
		ret i32 %c
	3:
		%d = i32 0
		ret i32 %d
1:
	%e = sub i32 %b, %a
	ret i32 %e
"""

class TestParser(unittest.TestCase):
	def test_add(self):
		add = "<result> = add <ty> <op1>, <op2>          ; yields ty:result\n"
		p = Parser(lines=add,debug=True)
		self.assertEqual(len(p.program),1)
		i0 = p.program[0]
		self.assertEqual(i0.__class__.__name__,"Add")
		self.assertEqual(i0.result, "<result>")
		self.assertEqual(i0.type,"<ty>")
		self.assertEqual(i0.arg1,"<op1>")
		self.assertEqual(i0.arg2,"<op2>")
	def test_sub(self):
		sub = "<result> = sub <ty> <op1>, <op2>          ; yields ty:result\n"
		p = Parser(lines=sub,debug=True)
		self.assertEqual(len(p.program),1)
		i0 = p.program[0]
		self.assertEqual(i0.__class__.__name__,"Sub")
		self.assertEqual(i0.result, "<result>")
		self.assertEqual(i0.type,"<ty>")
		self.assertEqual(i0.arg1,"<op1>")
		self.assertEqual(i0.arg2,"<op2>")
	def test_label(self):
		label = "Test:\n"
		p = Parser(lines=label,debug=True)
		self.assertEqual(len(p.program),1)
		i0 = p.program[0]
		self.assertEqual(i0.__class__.__name__,"Label")
		self.assertEqual(i0.name,"Test")
	def test_br(self):
		br = "br i1 <cond>, label <iftrue>, label <iffalse>\n"
		p = Parser(lines=br,debug=True)
		self.assertEqual(len(p.program),1)
		i0 = p.program[0]
		self.assertEqual(i0.__class__.__name__,"Br")
		self.assertEqual(i0.cond, "<cond>")
		self.assertEqual(i0.iftrue,"<iftrue>")
		self.assertEqual(i0.iffalse,"<iffalse>")
	def test_icmp(self):
		icmp = "<result> = icmp <cond> <ty> <op1>, <op2>   ; yields i1 or <N x i1>:result\n"
		p = Parser(lines=icmp,debug=True)
		self.assertEqual(len(p.program),1)
		i0 = p.program[0]
		self.assertEqual(i0.__class__.__name__,"Icmp")
		self.assertEqual(i0.result, "<result>")
		self.assertEqual(i0.cond_code,"<cond>")
		self.assertEqual(i0.type,"<ty>")
		self.assertEqual(i0.arg1,"<op1>")
		self.assertEqual(i0.arg2,"<op2>")
	def test_ret(self):
		ret = "ret <type> <value>       ; Return a value from a non-void function\n"
		p = Parser(lines=ret,debug=True)
		self.assertEqual(len(p.program),1)
		i0 = p.program[0]
		self.assertEqual(i0.__class__.__name__,"Ret")
		self.assertEqual(i0.type, "<type>")
		self.assertEqual(i0.arg1,"<value>")
	def test_label_cond_br_ret(self):
		p = Parser(lines=cond)
		self.assertEqual(len(p.program),9)
		p = p.program
		self.assertEqual(p[0].__class__.__name__,"Label")
		self.assertEqual(p[1].__class__.__name__,"Icmp")
		self.assertEqual(p[2].__class__.__name__,"Br")
		self.assertEqual(p[3].__class__.__name__,"Label")
		self.assertEqual(p[4].__class__.__name__,"Assign")
		self.assertEqual(p[5].__class__.__name__,"Ret")
		self.assertEqual(p[6].__class__.__name__,"Label")
		self.assertEqual(p[7].__class__.__name__,"Assign")
		self.assertEqual(p[8].__class__.__name__,"Ret")

class TestExec(unittest.TestCase):
	def test_cond(self):
		logging.basicConfig(level=logging.DEBUG)
		logging.debug("TestExec")
		p = Parser(lines=cond)
		e = Executor(p.program)
		logging.info("STARTING EXECUTION...")
		e.start(p.program[0])
		# logging.disable(logging.ERROR)
	def test_double_cond(self):
		logging.debug("TestExec2")
		p = Parser(lines=cond2)
		e = Executor(p.program)
		logging.info("STARTING EXECUTION...")
		e.start(p.program[0])
		logging.disable(logging.ERROR)

if __name__ == '__main__':
	unittest.main()