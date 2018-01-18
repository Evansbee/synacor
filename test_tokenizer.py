import ply.lex as lex


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
	'LABEL_DEF',
	'LABEL_REF',
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


def t_LABEL_DEF(t):
	r'[\.\:][a-zA-Z][a-zA-Z0-9_]+'
	if t.value[0] == ':':
		t.lexer.label_prefix = t.value[1:]
		t.value = t.value[1:]
	else:
		t.value = t.lexer.label_prefix + t.value
	return t


def t_LABEL_REF(t):
	r'[a-zA-Z][a-zA-Z0-9_]+(\.[a-zA-Z][a-zA-Z0-9_]+)?'
	if t.value in OPCODES:
		t.type = 'OPCODE'
		t.value = t.value
	elif t.value in REGISTERS:
		t.type = 'REGISTER'
		t.value = t.value
	elif t.value == 'db':
		t.type = 'DATA'
		t.value = t.value
	return t

def t_NUMBER(t):
	r'[0-9a-fA-F]+h|\d+'
	if t.value[-1] == 'h':
		t.value = int(t.value[:-1],16)
	else:
		t.value = int(t.value)
	return t

def t_PLACEMENT(t):
	r'@[0-9a-fA-F]+h|@\d+'
	if t.value[-1] == 'h':
		t.value = int(t.value[1:-1],16)
	else:
		t.value = int(t.value[1:])
	return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
	
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)	
	
t_ignore  = ' \t'	

	
data = r'''
@0000h         :init  jmp    init.jmp_0003
@0002h                halt   
						db 0234h
						db '2'
						db '321314'
@0003h     .jmp_0003  out    'bad\n'
@000Fh                out    ';'     ;helloasd asdasd 
@0007h                out    r0    ; tricky comments have 'this stuff' in them
@0090h 		jmp init.jmp_0003
'''

lexer = lex.lex()

	
lexer.input(data)
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)