''' Module used for assembly and disassembly of SYNACOR ASM/BIN files'''

from array import array
import ply.lex as lex
import ply.yacc as yacc





























#interface functions

def Assemble(text):
    return array('H')

def AssembleFile(filename):
    return array('H')

def Disassemble(bindata):
    return ""

def DisassembleFile(filename):
    return ""