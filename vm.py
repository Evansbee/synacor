
# coding: utf-8

# # Synacor Challenge - Collect all 8 Codes...
# This probable has to move to an actual console window in order to make the debugger

# In[1]:


from computer import Computer
from sys import exit
from array import array
import sys

def load_binary_data(computer, bindata):
    for i, data in enumerate(bindata):
        computer['memory'][i] = data
        
        
def load_binary_file(computer, binfile):
    with open(binfile, 'rb') as f:
        bindata = f.read()
        load_binary_data(computer,bindata)
        
def load_assembly_file(computer, asmfile):
    bindata = assemble_file(asmfile)
    load_binary_data(computer, bindata)

instruction_info = {
    'halt': {'op': 0, 'args': 0},
    'set': {'op': 1, 'args': 2},
    'push': {'op': 2, 'args': 1},
    'pop': {'op': 3, 'args': 1},
    'eq': {'op': 4, 'args': 3},
    'gt': {'op': 5, 'args': 3},
    'jmp': {'op': 6, 'args': 1},
    'jt': {'op': 7, 'args': 2},
    'jf': {'op': 8, 'args': 2},
    'add': {'op': 9, 'args': 3},
    'mul': {'op': 10, 'args': 3},
    'mod': {'op': 11, 'args': 3},
    'and': {'op': 12, 'args': 3},
    'or': {'op': 13, 'args': 3},
    'not': {'op': 14, 'args': 2},
    'rmem': {'op': 15, 'args': 2},
    'wmem': {'op': 16, 'args': 2},
    'call': {'op': 17, 'args': 1},
    'ret': {'op': 18, 'args': 0},
    'out': {'op': 19, 'args': 1},
    'in': {'op': 20, 'args': 1},
    'nop': {'op': 21, 'args': 0},
    'db' : {'op': None, 'args': 1}
}
def get_opcode(instr):
    if instr in instruction_info:
        return instruction_info[instr]['op']
    return None

opcode_info = {
    0: {'name': 'halt', 'args': 0},
    1: {'name': 'set', 'args': 2},
    2: {'name': 'push', 'args': 1},
    3: {'name': 'pop', 'args': 1},
    4: {'name': 'eq', 'args': 3},
    5: {'name': 'gt', 'args': 3},
    6: {'name': 'jmp', 'args': 1},
    7: {'name': 'jt', 'args': 2},
    8: {'name': 'jf', 'args': 2},
    9: {'name': 'add', 'args': 3},
    10: {'name': 'mul', 'args': 3},
    11: {'name': 'mod', 'args': 3},
    12: {'name': 'and', 'args': 3},
    13: {'name': 'or', 'args': 3},
    14: {'name': 'not', 'args': 2},
    15: {'name': 'rmem', 'args': 2},
    16: {'name': 'wmem', 'args': 2},
    17: {'name': 'call', 'args': 1},
    18: {'name': 'ret', 'args': 0},
    19: {'name': 'out', 'args': 1},
    20: {'name': 'in', 'args': 1},
    21: {'name': 'nop', 'args': 0}
}

def get_instr(opcode):
    if opcode in opcode_info:
        return opcode_info[opcode]
    return None
  
def reg_name(number):
    return ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7'][number - 32768]

def is_reg(number):
    return number >= 32768 and number <= 32775

def get_value(number, computer):
    if is_reg(number):
        return computer[reg_name(number)]
    else:
        return number

def get_value_string(number):
    if is_reg(number):
        return reg_name(number)
    else:
        return '{:04X}'.format(number)


# In[2]:




# In[62]:


op_code_map = {
        0:  {'inst':'halt', 'args':0, 'arg_types': [], 'help':'stop execution and terminate the program'},
        1:  {'inst':'set',  'args':2, 'arg_types': [['reg'],['reg','value']], 'help':'set register <a> to the value of <b>'},
        2:  {'inst':'push', 'args':1, 'arg_types': [['reg'],['value']], 'help':'push <a> onto the stack'},
        3:  {'inst':'pop',  'args':1, 'arg_types': [['reg']], 'help':'remove the top element from the stack and write it into <a>; empty stack = error'},
        4:  {'inst':'eq',   'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']], 'help':'set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise'},
        5:  {'inst':'gt',   'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']], 'help':'set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise'},
        6:  {'inst':'jmp',  'args':1, 'arg_types': [['reg','value']], 'help':'jump to <a>'},
        7:  {'inst':'jt',   'args':2, 'arg_types': [['reg','value'],['reg','value']], 'help':'if <a> is nonzero, jump to <b>'},
        8:  {'inst':'jf',   'args':2, 'arg_types': [['reg','value'],['reg','value']], 'help':'if <a> is zero, jump to <b>'},
        9:  {'inst':'add',  'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']], 'help':'assign into <a> the sum of <b> and <c> (modulo 32768)'},
        10: {'inst':'mul',  'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']], 'help':'store into <a> the product of <b> and <c> (modulo 32768)'},
        11: {'inst':'mod',  'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']],'help':'store into <a> the remainder of <b> divided by <c>'},
        12: {'inst':'and',  'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']],'help':'stores into <a> the bitwise and of <b> and <c>'},
        13: {'inst':'or',   'args':3, 'arg_types': [['reg'],['reg','value'],['reg','value']],'help':'stores into <a> the bitwise or of <b> and <c>'},
        14: {'inst':'not',  'args':2, 'arg_types': [['reg'],['reg','value']],'help':'stores 15-bit bitwise inverse of <b> in <a>'},
        15: {'inst':'rmem', 'args':2, 'arg_types': [['reg'],['reg','value']],'help':'read memory at address <b> and write it to <a>'},
        16: {'inst':'wmem', 'args':2, 'arg_types': [['reg','value'],['reg','value']],'help':'write the value from <b> into memory at address <a>'},
        17: {'inst':'call', 'args':1, 'arg_types': [['reg','value']],'help':'write the address of the next instruction to the stack and jump to <a>'},
        18: {'inst':'ret',  'args':0, 'arg_types': [],'help':'remove the top element from the stack and jump to it; empty stack = halt'},
        19: {'inst':'out',  'args':1, 'arg_types': [['reg','value']], 'help':'write the character represented by ascii code <a> to the terminal'},
        20: {'inst':'in',   'args':1, 'arg_types': [['reg']], 'help':'read a character from the terminal and write its ascii code to <a>'},
        21: {'inst':'nop',  'args':0, 'arg_types': [],'help':'no operation'},
    }

# ### Notes on ASM Format
# out 'long string' will be broken into individual outs
# label: jmp 12343 will be how labels are defined
# jmp [label] will indicate where they're used
# //will create an end of line comment
# .data 0x5234 will force replacement of those items, files will be read in order, this can screw everything up...
# 
# blank lines are discarded
# the assembler will preprocess everythign and dump out all excess garbage as a first pass
# 
# #### Additional Commands We're going To add
# dump a b will dump contents of memory to console a start address b is number of cells to dump
# 
# break will breakpoint 
# 
# sleep a will sleep for a milliseconds
# 
# labels should(must?) be 10 or less charcters and cannot be an opcode
# 
# \* in front of instruction sets a breakpoint on it (before it)
# 
# \*push a //has a breakpoint before pushing a
# 
# didn't do the break thing yet...
# 
# 
# labels support .label + 1 and .label - 1 (generic numbers)
# 
# 
# 

# In[17]:


def assemble_line(tokens, labels): #takes a token and converts to a string of bytes
    #returns {'label' : '', 'code':[1,2,3,4] }
    assembled_bytes = []
    if tokens['instruction'] in instruction_info and instruction_info[tokens['instruction']]['op'] != None:
        assembled_bytes += [instruction_info[tokens['instruction']]['op']]
    
    
    registers = ['r0','r1','r2','r3','r4','r5','r6','r7']
    for tok in tokens['args']:
        if tok in registers:
            assembled_bytes += [2**15 + registers.index(tok)]
        elif tok.startswith('.'):
            addition = 0
            if '+' in tok:
                thing = tok.split('+')    
                label = thing[0].lstrip('.')
                addition = int(thing[1])
            elif '-' in tok:
                thing = tok.split('-')    
                label = thing[0].lstrip('.')
                addition = -int(thing[1])
            else:
                label = tok.lstrip('.')
            
            if label in labels:
                assembled_bytes += [labels[label] + addition]
            else:
                print(label)
                print(labels)
                print("failed to assemble:",tokens)
                assembled_bytes += [0]
                exit()
        elif tok == "'": #work around bug, the parsers pulls the space on -> out ' '
            assembled_bytes += [ord(' ')]  
        elif tok == "'\\n'": #work around bug, the parsers pulls the space on -> out ' '
            assembled_bytes += [ord('\n')]  
        elif tok.startswith("'") and tok.endswith("'"):
            assembled_bytes += [ord(tok.strip("'"))]  
        else:
            assembled_bytes += [int(tok,16) % (2**15)]    
    return assembled_bytes


import re
def tokenize(line):
    parsed = dict()
    parsed['type'] = 'instruction'
    parsed['label'] = ''
    parsed['instruction'] = ''
    parsed['args'] = []
    parsed['comment'] = ''
    parsed['size'] = 0
    if '|' in line:
        line = line.split('|')[-1].rstrip().lstrip()
        if line == '':
            return None


    if line.startswith('@'):
        parsed['type'] = 'position'
        parsed['args'] = [line[1:]]
        return parsed

    make_tokens = re.compile(r'''\;[\w\s]*$|^\s*\w+\:|[\w\+\-\.]+|\'.\'|\'\\n\'''',re.VERBOSE).findall
    tokens = make_tokens(line)
    if tokens and tokens[0].endswith(':'):
        parsed['label'] = tokens[0][:-1].lstrip()
        tokens = tokens[1:]

    if tokens and tokens[0] in instruction_info :
        parsed['instruction'] = tokens[0]
        tokens = tokens[1:]
        
        if len(tokens) >= instruction_info[parsed['instruction']]['args']:
            parsed['args'] = [tokens[x] for x in range(instruction_info[parsed['instruction']]['args'])]
            tokens = tokens[instruction_info[parsed['instruction']]['args']:]
            if tokens and tokens[0].startswith(';'):
                tokens[0] = tokens[0].lstrip(';')
                parsed['comment'] = ' '.join(tokens)
            parsed['size'] = instruction_info[parsed['instruction']]['args']
            if instruction_info[parsed['instruction']]['op'] != None:
                parsed['size']  += 1
            
        else:
            print('err')
    elif tokens and tokens[0].startswith(';'):
        tokens[0] = tokens[0].lstrip(';')
        parsed['comment'] = ' '.join(tokens)
    elif not line or parsed['label']:
        pass
    else:
        print("Failed to tokenize:",line)
        print(line.split())
        print(tokens)
        exit()

    return parsed
    
    

def assemble_file(filename, debug = False):
    with open(filename) as f:
        asm_lines = f.read().splitlines()
        
        tokenized_lines = []
        current_address = 0
        current_offset = 0
        labels = dict()
        for asm_line in asm_lines:
            
            tl = tokenize(asm_line)
            print(tl)
            if tl:
                if tl['type'] == 'position':
                    current_offset = int(tl['args'][0],16)
                    current_address = 0

                
                if tl['label']:
                    labels[tl['label']] = current_address + current_offset
                tokenized_lines += [tl]
                current_address += tl['size']    
        
        binary_data = []
        for tok_line in tokenized_lines:
            #print('len:',len(binary_data),'tokenizing:',tok_line)

            if tok_line['type'] == 'position':
                fill_to = int(tok_line['args'][0],16)
                if fill_to < len(binary_data):
                    print("Can't achieve positional statement",tok_line,'size',len(binary_data))
                    print(tokenized_lines[:5])
                    exit()
                if fill_to == len(binary_data):
                    continue
                else:
                    binary_data += [21] * (fill_to - len(binary_data))

            else:
                binary_data += assemble_line(tok_line,labels)


        return binary_data#sum(binary_data, [])
    
#_ = assemble_file('dump.out')   
        


if __name__ == '__main__':
    #dis = disassemble('docs/challenge.bin', True)
    #with open('docs/challenge-details-clean.out','w') as f:
    #   f.write('\n'.join(dis))
    
    if len(sys.argv) > 1 and sys.argv[1] == 'disassemble':
        diasm = Computer.DisassembleFile('docs/challenge.bin')
        for _,x in diasm.items():
            if x['label'] != '':
                print('@{:04X} {:>12} {:6} {}'.format(x['start_address'],x['label']+':',x['op'],' '.join(x['processed_args'])))
            else:
                print('@{:04X} {:>12} {:6} {}'.format(x['start_address'],'',x['op'],' '.join(x['processed_args'])))
    elif len(sys.argv) > 2 and sys.argv[1] == 'assemble':
        test = assemble_file(sys.argv[2])   
    else:
        test = assemble_file('docs/challenge-working.out')   
        c = Computer()
        #c.load_program_from_file('docs/challenge.bin')
        c.load_program_from_data(test)


        for next_address in c.run():

            #sys.stdout.write('\r{:04X}'.format(next_address))
            #sys.stdout.flush()
            if c.output_buffer != '':
                print(c.output_buffer,end='')
                c.output_buffer = ''
            pass#print("PC: {:04X}".format(next_address))


    