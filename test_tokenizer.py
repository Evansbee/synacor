import ply.lex as lex
import ply.yacc as yacc

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

reserved = set(list(OPCODES.keys()) + list(REGISTERS.keys()) + ['db'])

tokens = [
	'NUMBER',
	'LABEL',
	'REFERENCE',
	'ANON_LABEL',
	'ANON_REFERENCE',
	'COMMENT',
	'PLUS',
	'MINUS',
	'LPAREN',
	'RPAREN',
	'CHAR',
	'STRING',
	'PLACEMENT',
	'OPCODE',
	'REGISTER',
	'DATA',
] + list(reserved)

t_CHAR = r"'.'"
t_STRING = r"'..+'|\"..+\""
t_PLUS = r'\+'
t_MINUS = r'\-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMENT = r';.*'
t_ANON_REFERENCE = r'\@b|\@f|\@r'

def t_LABEL(t):
	r'[a-zA-Z][a-zA-Z0-9_]{,9}:|\.[a-zA-Z][a-zA-Z0-9_]{,8}:'
	t.lexer.placement = False
	if t.value[0] != '.':
		t.lexer.label_prefix = t.value[:-1]
		t.value = t.value[:-1]
	else:
		t.value = t.lexer.label_prefix + t.value[:-1]
	return t

def t_ANON_LABEL(t):
	r'\@\@:'
	t.lexer.placement = False
	t.value = t.value[:-1]
	return t

def t_REFERENCE(t):
	r'[a-zA-Z][a-zA-Z0-9_]{,9}(\.[a-zA-Z][a-zA-Z0-9_]{,8})?|\.[a-zA-Z][a-zA-Z0-9_]{,8}'
	if t.value in OPCODES:
		t.lexer.placement = False
		t.type = 'OPCODE'
		t.value = t.value
	elif t.value in REGISTERS:
		t.type = 'REGISTER'
		t.value = t.value
	elif t.value == 'db':
		t.type = 'DATA'
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
0001h
0002h                halt   
						db 0234h
						db '2'
						db '321314'
0003h     .jmp_0003:  out    'bad\n'
000Fh                out    ';'     ;helloasd asdasd 
0007h                out    r0    ; tricky comments have 'this stuff' in them
0090h 		jmp .jmp_0003
jmp init
1000h     @@:   nop
jmp @b
jmp @r ;go back
jmp @f
'''

lexer = lex.lex()
lexer.placement = True
	
lexer.input(data)
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)


def p_empty(p):
	'empty :'
	print('EMPTY')

def p_program(p):
	'program : lines'
	print(p_program.__doc__)
	p[0] = Program(p[1])

def p_lines1(p):
	'lines : line lines'
	print(p_lines1.__doc__)
	p[0] = (p[1],) + p[2]

def p_lines2(p):
	'lines : line'
	print(p_lines2.__doc__)
	p[0] = (p[1],)

def p_line1(p):
	'line : location label operation comment'
	print(p_line1.__doc__)

def p_location(p):
	'location : PLACEMENT'
	'         | empty'
	print(p_location.__doc__)
	p[0] = Placement(p[1])

def p_labeldef(p):
	'label : LABEL'
	'      | ANON_LABEL'
	print(p_labeldef.__doc__)

def p_operation(p):
	'operation : OPCODE args'
	'          | empty'
	print(p_operation.__doc__)

def p_args1(p):
	'args : arg args'
	print(p_args1.__doc__)

def p_args2(p):
	'args : arg'
	print(p_args2.__doc__)	

def p_arg(p):
	'arg : NUMBER'
	'    | REGISTER'
	'    | REFERENCE'
	'    | ANON_REFERENCE'
	'    | CHAR'
	'    | STRING'
	'    | LPAREN expression RPAREN'
	'    | empty'
	print(p_arg.__doc__)	

def p_expression(p):
	'expression : NUMBER PLUS NUMBER'
	'           | REFERENCE PLUS NUMBER'
	'           | NUMBER PLUS REFERENCE'
	'           | NUMBER MINUS NUMBER'
	'           | REFERENCE MINUS NUMBER'
	'           | NUMBER MINUS REFERENCE'
	print(p_expression.__doc__)

def p_comment(p):
	'comment : COMMENT'
	'        | empty'
	print(p_comment.__doc__)

def p_error(p):
	print('Parse error')



class Program(object):
	def __init__(self):
		pass
	def assemble(self):
		pass
	def pretty_print(self):
		pass	

class Line(object):
	def __init__(self):
		pass
	def assemble(self):
		pass
	def pretty_print(self):
		pass	

class Comment(object):
	def __init__(self):
		pass
	def assemble(self):
		pass
	def pretty_print(self):
		pass	

class Opcode(object):
	def __init__(self):
		pass
	def assemble(self):
		pass
	def pretty_print(self):
		pass	

class Arg(object):
	def __init__(self):
		pass
	def assemble(self):
		pass
	def pretty_print(self):
		pass	

class Label(object):
	def __init__(self):
		pass
	def assemble(self):
		pass
	def pretty_print(self):
		pass	



parser = yacc.yacc()

result = parser.parse(data, lexer=lexer)
print(result)