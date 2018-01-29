''' Module used for assembly and disassembly of SYNACOR ASM/BIN files'''

from array import array
import ply.lex as lex
import ply.yacc as yacc
import sys

from collections import OrderedDict

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
	'mul' : 10,
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

MNEUMONICS = dict((v,k) for k,v in OPCODES.items())
REV_REGISTERS = dict((v,k) for k,v in REGISTERS.items())
ARGCOUNT = array('B', [0,2,1,1,3,3,1,2,2,3,3,3,3,3,2,2,2,1,0,1,1,0])   

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
    if t.value[0] != '.' and t.value != '@@:': #don't change prefix for anon
        t.lexer.label_prefix = t.value[:-1]
        t.value = t.value[:-1]
    elif t.value[0] != '.':
        t.value = t.value[:-1]
    else:
        t.value = t.lexer.label_prefix + t.value[:-1]
    return t

def t_REGISTER(t):
    r'r[0-7]'
    t.value = REGISTERS[t.value]
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
    r'0x[0-9a-fA-F]+|[0-9a-fA-F]+h|\d+'
    if t.value[-1] == 'h':
        t.value = int(t.value[:-1],16)
    elif len(t.value) > 2 and t.value[0:2] == '0x':
        t.value = int(t.value[2:],16)
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

def find_next(array_of_locations, value):
    if len(array_of_locations) == 0:
        return None

    for v in array_of_locations:
        if v > value:
            return v
    return None

def find_previous(array_of_locations, value):
    if len(array_of_locations) == 0:
        return None

    last = None
    for v in array_of_locations:
        if v > value:
            return last
        last = v

    return Last

def pretty_string(val):
	if not isinstance(val,int):
		return val
	if chr(val) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-=+_!@#$%^&*()[]{}\|;\':",.<>/?`~"':
		return "'" + chr(val) + "'"
	elif val < REGISTERS['r0']:
		return "0x{:04x}".format(val)
	elif val <= REGISTERS['r7']:
		return "r{}".format(val-REGISTERS['r0'])
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
                    self.labels[line.label.name] = self.size

            self.size += line.size

    def assemble(self):
        data = array('H')
        current_location = 0
        for line in self.lines:
            if line.placement > current_location:
                data.extend(array('H',[21] * (line.placement - current_location)))
                current_location = line.placement
            data.extend(line.assemble(current_location, self.labels, self.anon_labels))
            current_location += line.size
        return data

    def pretty(self, verbose = False):
        current_location = 0
        out = ""
        for line in self.lines:
            data = ""
            pretty = line.pretty()
            if verbose:
                if line.placement > current_location:
                    current_location = line.placement
                pretty += '\n; ASSEMBLED AS -> ' + " ".join(["0x{:04x}".format(x) for x in line.assemble(current_location, self.labels, self.anon_labels)]) + '\n'
            out += pretty + '\n'
        return out	

class Line(object):
    def __init__(self, placement, label, operation, comment):
        self.placement = placement
        self.line_number = -1
        self.label = label
        self.operation = operation
        self.comment = comment
        self.size = 0
        if self.operation:
            self.size = self.operation.size		

    def assemble(self, current_location, labels = {}, anon_labels = []):
        if self.operation:
            return self.operation.assemble(current_location,labels,anon_labels)
        else:
            return array('H')
    def __str__(self):
        out = "line:{} -> {}".format(self.line_number,self.pretty())
        return out
    
    def __repr__(self):
        out = "line:{} -> {}".format(self.line_number,self.pretty())  
        return out


    def pretty(self):
        placement = ""
        label = ""
        operation = ""
        comment = ";" + str(self.line_number)
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
        self.is_anon = name in ['@f','@r','@b']
        self.name = name
        self.size = 1

    def assemble(self, current_location, labels = {}, anon_labels = []):
        if self.is_anon:
            if self.name in ['@r','@b']:
                return array('H',[find_previous(anon_labels,current_location)])
            else:
                return array('H',[find_next(anon_labels,current_location)])    
        else:
            return array('H',[labels[self.name]])

    def pretty(self):
        return self.name


class Operation(object):
    def __init__(self, opcode, args = []):
        self.op = opcode
        self.args = args
        self.size = 0
        if self.op == 'db':
            self.size = len(args)
        elif self.op == 'out':
            self.size = 2 * self.args[0].size
        else:
            self.size = 1 + len(self.args)
        

    def assemble(self, current_location, labels = {}, anon_labels = []):
        data = array('H')
        if self.op == 'db':
            for a in self.args:
                data.extend(a.assemble(current_location,labels,anon_labels))
        elif self.op != 'out':
            data.extend(array('H',[OPCODES[self.op]]))
            for a in self.args:
                data.extend(a.assemble(current_location, labels,  anon_labels))
        else:
            assert(len(self.args) == 1)
            string_data = self.args[0].assemble(current_location, labels,  anon_labels)
            for d in string_data:
                data.extend(array('H',[OPCODES[self.op], d]))

        return data


    def pretty(self):
        ret = self.op + ' '
        for arg in self.args:
            ret += arg.pretty() + ' '
        return ret	

class Register(object):
    def __init__(self, r_value):
        self.reg = r_value
        self.size = 1
    
    def assemble(self, current_location, labels = {}, anon_labels = []):
        return array('H',[self.reg])

    def pretty(self):
        return REV_REGISTERS[self.reg]	

class Expression(object):
    def __init__(self, arg_a, op, arg_b):
        self.size = 1
        self.a = arg_a
        self.op = op
        self.b = arg_b
        
    def assemble(self, current_location, labels = {}, anon_labels = []):
        a = self.a.assemble(current_location, labels, anon_labels)
        b = self.b.assemble(current_location, labels, anon_labels)
        if self.op == '+':
            return array('H',[a[0]+b[0]])
        

        if self.op == '-':
            return array('H',[a[0]-b[0]])


    def pretty(self):
        return '({}{}{})'.format(self.a.pretty(),self.op,self.b.pretty())

class Char(object):
    def __init__(self, char):
        self.char = char
        self.size = 1
		    
    def assemble(self, current_location, labels = {}, anon_labels = []):
        return array('H', [ord(self.char)])

    def pretty(self):
        if self.char == '\n':
            temp = '\\n'
        else:
            temp = self.char
        return "'" + temp + "'"

class String(object):
    def __init__(self, string):
        self.string = string
        self.size = len(self.string)

    def assemble(self, current_location, labels = {}, anon_labels = []):
        return array('H', [ord(x) for x in self.string])

    def pretty(self):
        temp = self.string.replace('\n','\\n')
        return "'" + temp + "'"

class Literal(object):
    def __init__(self, value):
        self.value = value
        
    def assemble(self, current_location, labels = {}, anon_labels = []):
        return array('H', [self.value])
            
    def make_ref(self, label):
        return Reference(label)
    
    def pretty(self):
        return pretty_string(self.value)
        


class Number(object):
    def __init__(self, number):
        self.number = number
        self.size = 1
        
    def assemble(self, current_location, labels = {}, anon_labels = []):
        return array('H', [self.number])

    def pretty(self):
        return pretty_string(self.number)


class Label(object):
    def __init__(self, name):
        self.name = name

    def pretty(self):
        return self.name +":"	

def p_program(p):
    'program : lines' 
    p[0] = Program(p[1])

def p_lines1(p):
    'lines : line lines'	
    p[1].line_number = p.lineno(0)
    p[0] = [p[1]] + p[2]

def p_lines2(p):
    'lines : line'
    p[1].line_number = p.lineno(0)
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
    'line : operation'
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
            | MUL args
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
	p[0] = Number(p[1])

def p_arg_reg(p):
	'arg : REGISTER'
	p[0] = Register(p[1])

def p_arg_ref(p):
	'arg : REFERENCE'
	p[0] = Reference(p[1])

def p_arg_char(p):
    'arg : CHAR'
    string = str(p[1])[1:-1]
    string = string.replace('\\n','\n')
    p[0] = Char(string)

def p_arg_string(p):		   
    'arg : STRING'
    string = str(p[1])[1:-1]
    string = string.replace('\\n','\n')
    if len(string) == 1: #this covers the literal coming in as \\n instead of just \n
        p[0] = Char(string)
    else:
        p[0] = String(string)

def p_arg_expression(p):
	'''arg : LPAREN expression RPAREN'''
	p[0] = p[2]

def p_expression_nmn(p):
    'expression : NUMBER MATHOP NUMBER'
    p[0] = Expression(Number(p[1]),p[2],Number(p[3]))

def p_expression_rmn(p):
    'expression : REFERENCE MATHOP NUMBER'
    p[0] = Expression(Reference(p[1]),p[2],Number(p[3]))

def p_expression_nmr(p):
    'expression : NUMBER MATHOP REFERENCE'
    p[0] = Expression(Number(p[1]),p[2],Reference(p[3]))

def p_error(p):
	if p:
		print('Syntax Error at token', p.type, p.lineno(0))
		sys.exit()
	else:
		print('Syntax Error')
		sys.exit()

def p_empty(p):
	'empty :'
	pass

def make_lexer():
    lexer = lex.lex()
    lexer.placement = True
    lexer.lineno = 1
    return lexer

def make_parser():
    parser = yacc.yacc(debug = False)#, write_tables = False)
    return parser

def Parse(text):
    lexer = make_lexer()
    parser = make_parser()
    program = parser.parse(text,lexer=lexer, tracking = True)
    program.text = text
    return program

def ParseFile(filename):
    text = ""
    with open(filename) as f:
        text = f.read()
    return Parse(text)

def Pretty(text, verbose = False):
    prog = Parse(text)
    return (prog.pretty(verbose), prog)

def PrettyFile(filename, verbose = False):
    prog = ParseFile(filename)
    return (prog.pretty(verbose), prog)

def Assemble(text):
    prog = Parse(text)
    return (prog.assemble(), prog)

def AssembleFile(filename):
    prog = ParseFile(filename)
    return (prog.assemble(), prog)




# HERE COMES THE HOST MESS SECTION


def isreg(val):
    return val in REV_REGISTERS


def valid_instruction(op_args):
    if op_args[0] >= 0 and op_args[0] <= 22:
        op = op_args[0]
        args = op_args[1:]
        
        if len(args) != ARGCOUNT[op]:
            return False
        
        if op == 0:
            return True
        elif op == 1: #set
            return isreg(args[0]) and args[1] < 32776
        elif op == 2: #push
            return args[0] < 32776
        elif op == 3: #pop
            return isreg(args[0])
        elif op == 4: #eq
            return isreg(args[0]) and args[1] < 32776 and args[2] < 32776
        elif op == 5: #gt
            return isreg(args[0]) and args[1] < 32776 and args[2] < 32776
        elif op == 6: #jmp
            return args[0] < 32776
        elif op == 7: #jt
            return args[0] < 32776 and args[1] < 32776
        elif op == 8: #jf
            return args[0] < 32776 and args[1] < 32776
        elif op == 9 or op == 10 or op == 11 or op == 12 or op == 13: #add, mult, mod, and, or
            return isreg(args[0]) and args[1] < 32776 and args[2] < 32776
        elif op == 14: #not
            return isreg(args[0]) and args[1] < 32776
        elif op == 15: #rmem
            return isreg(args[0]) and args[1] < 32776
        elif op == 16: #wmem
            return args[0] < 32776 and args[1] < 32776
        elif op == 17: #call
            return args[0] < 32776
        elif op == 18: #ret
            return True
        elif op == 19: #out
            return args[0] < 32776
        elif op == 20: #in
            return isreg(args[0])
        elif op == 21: #nop
            return True
        else:
            return False #no reach
    else:
        return False
    return False #no reach

def reg_or_value_string(val):
    if isreg(val):
        return REV_REGISTERS[val]
    elif chr(val) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-=+_!@#$%^&*()[]{}\|;\':",.<>/?`~"':
        return "'" + chr(val) + "'"
    else:
        return '0x{:04X}'.format(val)

def Disassemble(data, verbose = False):
    disassembly = OrderedDict()
    file_size = len(data)
    addr = 0
    lines = []
    labels = {0:'init'}
    while addr < file_size:
        token = dict()
        token['start_address'] = addr
    
        if token['start_address'] in labels:
            token['label'] = labels[token['start_address']]
            del(labels[token['start_address']])
        else:
            token['label'] = ''            

        if data[addr] in MNEUMONICS and valid_instruction(data[addr:1+addr+ARGCOUNT[data[addr]]]):
            
            actual_values = data[addr:1+addr+ARGCOUNT[data[addr]]]
            addr += len(actual_values)

            token['op'] = MNEUMONICS[actual_values[0]]
            
            token['args'] = actual_values[1:]
            token['raw'] = actual_values
            token['size'] = len(actual_values)
            token['processed_args'] = []
            token['comment'] = ''

            for arg in token['args']:
                token['processed_args'] += [reg_or_value_string(arg)]

            def update_label(addr, prefix, token, offset):
                if token['start_address'] < addr:
                    labels[addr] = "{}_{:04X}".format(prefix,addr)
                    token['processed_args'][offset] = "{}_{:04X}".format(prefix,addr)
                elif addr in disassembly and disassembly[addr]['label'] == '':
                    disassembly[addr]['label'] = "{}_{:04X}".format(prefix,addr)
                    token['processed_args'][offset] = "{}_{:04X}".format(prefix,addr)
                elif addr not in disassembly:
                    pass
                else:
                    token['processed_args'][offset] = disassembly[addr]['label']

            if token['op'] == 'jmp' and not isreg(actual_values[1]):
                update_label(actual_values[1],'jmp',token, 0)
            elif (token['op'] == 'jnz' or token['op'] == 'jz' ) and not isreg(actual_values[2]):
                update_label(actual_values[2],'jmp',token, 1)
            elif token['op'] == 'call' and not isreg(actual_values[1]):
                update_label(actual_values[1],'sub',token, 0)
            elif token['op'] == 'rmem' and not isreg(actual_values[2]):
                update_label(actual_values[2],'mem',token, 1)
            elif token['op'] == 'wmem' and not isreg(actual_values[1]):
                update_label(actual_values[1],'mem',token, 0)
            elif token['op'] == 'out' and actual_values[1] < 255:
                if actual_values[1] == 10:
                    token['processed_args'][0] = r"'\n'"
                else:
                    token['processed_args'][0] = r"'{}'".format(chr(actual_values[1]))


            #check valid
            if valid_instruction(actual_values):
                disassembly[token['start_address']] = token
            else:
                print("DROPPING",token)
            
        else:
            actual_values = [data[addr]]
            addr += 1
            token['op'] = 'db'
            token['args'] = actual_values
            token['raw'] = actual_values
            token['size'] = 1
            token['processed_args'] = ['0x{:04x}'.format(actual_values[0])]
            token['comment'] = ''
            disassembly[token['start_address']] = token
    return disassembly


def DisassembleFile(program_file, verbose = False):
    
    # 00HHHH  |  HHHH HHHH HHHH HHHH  |  asm__opa, opb, opc 

    with open(program_file,'rb') as f:            
        data  = array('H')
        try:
            data.fromfile(f,2**16)
        except EOFError:
            pass
        return Disassemble(data,verbose)
    return []