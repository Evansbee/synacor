import ply.lex as lex

reserved = ['']

tokens = (
	'NUMBER',
	'GLOBALLABEL',
	'LOCALLABEL',
	'FQLABEL',
	'OPCODE',
	'REGISTER',
	'COMMENT',
	'PLUS',
	'MINUS',
	'LPAREN',
	'RPAREN',
	'CHAR',
	'STRING',
	'PLACEMENT'
)

t_CHAR = r"'.'"
t_STRING = r"'..+'|\"..+\""
t_PLUS = r'\+'
t_MINUS = r'\-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_REGISTER = r'r[0-7]'
t_OPCODE = r'halt|set|push|pop|eq|gt|jmp|jnz|jz|add|mult|mod|and|or|not|rmem|wmem|call|ret|out|in|nop|db'
t_LOCALLABEL = r'\.[a-zA-Z][a-zA-Z0-9_]+'
t_GLOBALLABEL = r'\:[a-zA-Z][a-zA-Z0-9_]+'
t_FQLABEL = r'\:[a-zA-Z][a-zA-Z0-9\_]+\.[a-zA-Z][a-zA-Z0-9_]+'
t_COMMENT = r';.*'

def t_PLACEMENT(t):
	r'^[0-9a-fA-F]+h|^\d+'
	if t.value[-1] == 'h':
		t.value = int(t.value[:-1],16)
	else:
		t.value = int(t.value)
	return t
	
def t_NUMBER(t):
	r'[0-9a-fA-F]+h|\d+'
	if t.value[-1] == 'h':
		t.value = int(t.value[:-1],16)
	else:
		t.value = int(t.value)
	return t


	
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
	
def t_newline(t):
	r'\n+'
	print('NEWLINE')
	t.lexer.lineno += len(t.value)	
	
t_ignore  = ' \t'	

	
data = '''
0000h         :init  jmp    .jmp_0003
0002h                halt   
0003h     .jmp_0003  out    'bad'
000Fh                out    ';'     ;helloasd asdasd 
0007h                out    r0    ; tricky comments have 'this stuff' in them
jmp :init.jmp_0003
'''

lexer = lex.lex()

	
lexer.input(data)
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)