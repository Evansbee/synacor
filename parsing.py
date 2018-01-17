from pyparsing import *

'''
asm
line ::= [placement] [label] [opcode args

'''


test_asm_lines = [
    "0012",
    "test: nop",
    "nop",
    "set r0 r1",
    "nop ; a thing",
    "ABCD test: nop; hi",
]
positional = Word(hexnums, exact = 4)
label = Word(alphas, exact = 1) + Word(alphanums + "_",max=9)
opcode = Literal('nop') ^ Literal('set') ^ Literal('jmp')
refLabel = '.' + Word(alphas, exact = 1) + Word(alphanums + "_",max=9)
#args = Or()

par = Optional(Word(hexnums)) + Optional(Word(alphas, max=1) + Word(alphanums + "_") + ':') + Optional(Or('nop','set')) + Optional(Group(';' + restOfLine))


for asm in test_asm_lines:
    print(par.parseString(asm))