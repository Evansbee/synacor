import ply.lex as lex
import ply.yacc as yacc
import sys
OPCODES = {
	'halt' : 0,
	'set'  : 1,
	'push' : 2,
	'pop'  : 3,
	'eq'   : 4,
	'gt'   : 5,
	'jmp'  : 6,
	'jnz'  : 7,
	'jz'   : 8,
	'add'  : 9,
	'mult' : 10,
	'mod'  : 11,
	'and'  : 12,
	'or'   : 13,
	'not'  : 14,
	'rmem' : 15,
	'wmem' : 16,
	'call' : 17,
	'ret'  : 18,
	'out'  : 19,
	'in'   : 20,
	'nop'  : 21,
}

REGISTERS = {
	'r0' : 32768,
	'r1' : 32769,
	'r2' : 32770,
	'r3' : 32771,
	'r4' : 32772,
	'r5' : 32773,
	'r6' : 32774,
	'r7' : 32775
}

reserved = set(list(OPCODES.keys()) + ['db'])

tokens = list(x.upper() for x in reserved) + [
	'NUMBER',
	'LABEL',
	'REFERENCE',
	'COMMENT',
	'MATHOP',
	'LPAREN',
	'RPAREN',
	'CHAR',
	'STRING',
	'PLACEMENT',
	'REGISTER',
]

t_CHAR = r"'.'"
t_STRING = r"'[^']{2,}'|\"[^\"]{2,}\""
t_MATHOP = r'[\-\+]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMENT = r';.*'

def t_LABEL(t):
	r'[a-zA-Z][a-zA-Z0-9_]{,9}:|\.[a-zA-Z][a-zA-Z0-9_]{,8}:|\@\@:'
	t.lexer.placement = False
	if t.value[0] != '.':
		t.lexer.label_prefix = t.value[:-1]
		t.value = t.value[:-1]
	else:
		t.value = t.lexer.label_prefix + t.value[:-1]
	return t

def t_REGISTER(t):
	r'r[0-7]'
	return t

def t_REFERENCE(t):
	r'[a-zA-Z][a-zA-Z0-9_]{,9}(\.[a-zA-Z][a-zA-Z0-9_]{,8})?|\.[a-zA-Z][a-zA-Z0-9_]{,8}|\@f|\@b|\@r'
	if t.value in OPCODES:
		t.lexer.placement = False
		t.type = t.value.upper()
		t.value = t.value
	elif t.value == 'db':
		t.lexer.placement = False
		t.type = 'DB'
		t.value = t.value
	elif t.value[0] == '.': #local label
		t.value = t.lexer.label_prefix + t.value
	return t

def t_NUMBER(t):
	r'[0-9a-fA-F]+h|\d+|0x[0-9a-fA-F]+'
	if t.value[-1] == 'h':
		t.value = int(t.value[:-1],16)
	else:
		t.value = int(t.value)
	if t.lexer.placement:
		t.lexer.placement = False
		t.type = 'PLACEMENT'	
	return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
	
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)	
	t.lexer.placement = True
	
t_ignore  = ' \t'	

	
data = r'''
0000h         init:  jmp    init.jmp_0003
20 ;blankish line
40                halt   
						db 0234h 20 55
						db '2'
						db '321314'
100h     .jmp_0003:  out    'bad\n'
200h                out    ';'     ;helloasd asdasd 
300h                out    r0    ; tricky comments have 'this stuff' in them
			set r0 123
			add r0 r1 (@f+1)

400h 		jmp .jmp_0003
jmp init
1000h     @@:   nop
jmp @b
jmp @r ;go back
jmp @f
@@: nop
'''

def pretty_string(val):
	if not isinstance(val,int):
		return val

	if chr(val) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-=+_!@#$%^&*()[]{}\|;\':",.<>/?`~"':
		return "'" + chr(val) + "'"
	elif val < REGISTERS['r0']:
		return "0x{:04x}".format(val)
	elif val <= REGISTER['r7']:
		return "r{}".format(val-REGISTER['r0'])
	else:
		return val

class Program(object):
	def __init__(self, lines):
		self.lines = []
		self.labels = {}
		self.anon_labels = []
		self.size = 0
		for line in lines:
			self.lines.append(line)
			if line.placement:
				if self.size > line.placement:
					raise Exception('Invalid Placement')
					sys.exit()
				self.size = line.placement
			else:
				line.placement = self.size
			
			if line.label:
				if line.label.name == '@@':
					self.anon_labels += [self.size]
				else:
					self.labels[self.size] = line.label.name

			self.size += line.size
	
	def assemble(self):
		pass
	def pretty(self):
		return '\n'.join([line.pretty() for line in self.lines])	

class Line(object):
	def __init__(self, placement, label, operation, comment):
		self.placement = placement
		self.label = label
		self.operation = operation
		self.comment = comment
		self.size = 0
		if self.operation:
			self.size = self.operation.size

		print("LINE: ",placement, label, operation, comment)
		pass
	def assemble(self, labels = {}, anon_labels = []):
		pass

	def __str__(self):
		print(self.pretty())
	def __repr__(self):
		print(self.pretty())	


	def pretty(self):
		placement = ""
		label = ""
		operation = ""
		comment = ""
		if self.placement is not None:
			placement = "0x{:04x}".format(self.placement)
		if self.label:
			label = self.label.pretty()
		if self.operation:
			operation = self.operation.pretty()
		if self.comment:
			comment = self.comment.pretty()	
		return "{:8}{:>20}  {:30}{}".format(placement,label,operation,comment)

class Comment(object):
	def __init__(self, comment):
		self.comment = comment.lstrip(';').lstrip()
	def pretty(self):
		return '; ' + self.comment	


class Reference(object):
	def __init__(self, name):
		self.name = name
	def assemble(self, labels = {}, anon_labels = []):
		pass
	def pretty(self):
		return self.name


class Operation(object):
	def __init__(self, opcode, args = []):
		self.op = opcode
		self.args = args
		self.size = 10

	def assemble(self, labels = {}, anon_labels = []):
		pass
	def pretty(self):
		ret = self.op + ' '
		for arg in self.args:
			ret += arg.pretty() + ' '
		return ret	

class Register(object):
	def __init__(self, name):
		self.name = name
		pass
	def assemble(self, labels = {}, anon_labels = []):
		pass
	def pretty(self):
		return self.name	

class Expression(object):
	def __init__(self, arg_a, op, arg_b):
		self.a = arg_a
		self.op = op
		self.b = arg_b
		
	def assemble(self, labels = {}, anon_labels = []):
		pass
	def pretty(self):
		return '({}{}{})'.format(self.a,self.op,self.b)

class Arg(object):
	def __init__(self, arg):
		self.arg = arg
		pass
	def assemble(self, labels = {}, anon_labels = []):
		if isinstance(self.arg, Expression) or isinstance(self.arg,Register) or isinstance(self.arg, Reference):
			return [self.arg.assemble(labels, anon_labels)]
		elif isinstance(self.arg, int):
			return [self.arg]
		elif isinstance(self.arg, str):
			return [ord(x) for x in self.arg]

	def pretty(self):
		if isinstance(self.arg, Expression) or isinstance(self.arg,Register) or isinstance(self.arg, Reference):
			return self.arg.pretty()
		elif isinstance(self.arg, int):
			return pretty_string(self.arg)
		else:
			return self.arg	

class Label(object):
	def __init__(self, name):
		self.name = name
		pass
	def pretty(self):
		return self.name +":"	

lexer = lex.lex()
lexer.placement = True
	
#lexer.input(data)
#while True:
#	tok = lexer.token()
#	if not tok: 
#		break      # No more input
#	print(tok)



def p_program(p):
	'program : lines'
	p[0] = Program(p[1])
	#p[0] = p[1]

def p_lines1(p):
	'lines : line lines'	
	p[0] = [p[1]] + p[2]

def p_lines2(p):
	'lines : line'
	p[0] = [p[1]]

def p_line_ploc(p):
	'line : PLACEMENT LABEL operation COMMENT'
	p[0] = Line(p[1],Label(p[2]),p[3],Comment(p[4]))


def p_line_loc(p):
	'line : LABEL operation COMMENT'
	p[0] = Line(None,Label(p[1]),p[2],Comment(p[3]))

def p_line_poc(p):
	'line : PLACEMENT operation COMMENT'
	p[0] = Line(p[1],None,p[2],Comment(p[3]))

def p_line_plc(p):
	'line : PLACEMENT LABEL COMMENT'
	p[0] = Line(p[1],Label(p[2]),None,Comment(p[3]))

def p_line_plo(p):
	'line : PLACEMENT LABEL operation'
	p[0] = Line(p[1],Label(p[2]),p[3],None)


def p_line_oc(p):
	'line : operation COMMENT'
	p[0] = Line(None,None,p[1],Comment(p[2]))


def p_line_pc(p):
	'line : PLACEMENT COMMENT'
	p[0] = Line(p[1],None,None,Comment(p[2]))

def p_line_pl(p):
	'line : PLACEMENT LABEL '
	p[0] = Line(p[1],Label(p[2]),None,None)


def p_line_lc(p):
	'line : LABEL COMMENT'
	p[0] = Line(None,Label(p[1]),None,Comment(p[2]))

def p_line_po(p):
	'line : PLACEMENT operation '
	p[0] = Line(p[1],None, p[2] ,None)

def p_line_lo(p):
	'line : LABEL operation'
	p[0] = Line(None, Label(p[1]),p[2] ,None)

def p_line_p(p):
	'line : PLACEMENT'
	p[0] = Line(p[1],None, None, None)

def p_line_l(p):
	'line : LABEL '
	p[0] = Line(None, Label(p[1]), None, None)

def p_line_o(p):
	'line : operation '
	p[0] = Line(None, None, p[1], None)


def p_line_c(p):
	'line : COMMENT'
	p[0] = Line(None, None, None, Comment(p[1]))

def p_line_e(p):
	'line : empty'
	pass


def p_operation(p):
	'''operation : HALT
	          | SET args
	          | PUSH args
	          | POP args
	          | EQ args
	          | GT args
	          | JMP args
	          | JNZ args
	          | JZ args
	          | ADD args
	          | MULT args
	          | MOD args
	          | AND args
	          | OR args
	          | NOT args
	          | RMEM args
	          | WMEM args
	          | CALL args
	          | RET
	          | OUT args
	          | IN args
	          | NOP
			  | DB args'''

	if len(p) > 2:
		p[0] = Operation(p[1],p[2])
	else:
		p[0] = Operation(p[1], [])

def p_args1(p):
	'''args : arg args'''
	p[0] = [p[1]] + p[2]

def p_args2(p):
	'''args : arg'''
	p[0] = [p[1]]

def p_arg_num(p):
	'arg : NUMBER'
	p[0] = Arg(p[1])

def p_arg_reg(p):
	'arg : REGISTER'
	p[0] = Register(p[1])

def p_arg_ref(p):
	'arg : REFERENCE'
	p[0] = Reference(p[1])

def p_arg_char(p):
	'arg : CHAR'
	p[0] = Arg(p[1])

def p_arg_string(p):		   
	'arg : STRING'
	p[0] = Arg(p[1])

def p_arg_expression(p):
	'''arg : LPAREN expression RPAREN'''
	p[0] = Arg(p[2])

def p_expression(p):
	'''expression : NUMBER MATHOP NUMBER
	           | REFERENCE MATHOP NUMBER
	           | NUMBER MATHOP REFERENCE'''
	p[0] = Expression(p[1],p[2],p[3])

def p_error(p):
	if p:
		print('Syntax Error at token', p.type)
		sys.exit()
	else:
		print('Syntax Error')
		sys.exit()

def p_empty(p):
	'empty :'
	pass





parser = yacc.yacc(debug = False, write_tables = False)
result = parser.parse(data, lexer=lexer)
print(result.pretty())
print(result.labels)
print(result.anon_labels)