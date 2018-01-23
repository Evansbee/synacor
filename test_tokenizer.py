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



def p_program(p):
	'program : lines'
	print("PROGRAM")

def p_lines1(p):
	'lines : line lines'	
	p[0] = (p[1],) + p[2]

def p_lines2(p):
	'lines : line'
	p[0] = (p[1],)

def p_line1(p):
	'line : location label operation comment'
	print('LINE')

def p_location(p):
	'''location : PLACEMENT
	         | empty'''
	if p[1]: print('PLACE',p[1])
	#p[0] = Placement(p[1])

def p_label(p):
	'''label : LABEL
	      | empty'''
	if p[1]: print('LABEL',p[1])

def p_operation(p):
	'''operation : HALT
	          | SET REGISTER arg
	          | PUSH REGISTER
	          | POP REGISTER
	          | EQ REGISTER arg arg
	          | GT REGISTER arg arg
	          | JMP arg
	          | JNZ arg arg
	          | JZ arg
	          | ADD REGISTER arg arg
	          | MULT REGISTER arg arg
	          | MOD REGISTER arg arg
	          | AND REGISTER arg arg
	          | OR REGISTER arg arg
	          | NOT REGISTER arg
	          | RMEM REGISTER arg
	          | WMEM REGISTER arg
	          | CALL arg
	          | RET
	          | OUT arg
	          | IN REGISTER
	          | NOP
				 | DB args
	          | empty'''

	if p[1]: print('OP', p[1])

def p_args(p):
	'''args : arg args
	        | arg'''
	print('ARG',p[1])

def p_arg(p):
	'''arg : NUMBER
	    | REGISTER
	    | REFERENCE
	    | CHAR
	    | STRING
	    | LPAREN expression RPAREN'''
	print('ARG',p[1])

def p_expression(p):
	'''expression : NUMBER MATHOP NUMBER
	           | REFERENCE MATHOP NUMBER
	           | NUMBER MATHOP REFERENCE'''
	print(p[1],p[2],p[3])

def p_comment(p):
	'''comment : COMMENT
	        | empty'''
	if p[1]: print('COMMENT',p[1])

def p_error(p):
	print('Parse error', p)

def p_empty(p):
	'empty :'
	pass


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
#print(result)