from array import array
from collections import OrderedDict
import re
import datetime
import time
from ctypes import *
import os

dll = CDLL(os.path.realpath(os.path.join(os.path.dirname(__file__), 'emu')))

class cEmulator(Structure):
    _fields_ = [
        ('pc', c_ushort),
        ('registers', c_ushort * 8),
        ('memory', c_ushort * 0x7FFF),
        ('breakpoints', c_ushort * 64),
        ('breakpoints_write_pointer',c_ushort),
        ('stack', c_ushort * 1000),
        ('stack_write_pointer', c_ushort),
        ('cycles',c_ulonglong),
        ('input_buffer',c_char * 2048),
        ('output_buffer',c_char * 2048),
        ('halted',c_int),
        ('program_loaded',c_int),
        ('waiting_for_input', c_int),
        ('output_buffer_full', c_int),
        ('stack_overflow', c_int)
        ('at_breakpoint', c_int)
    ]

FIELDS = set(x[0] for x in cEmulator._fields_)    

OPCODES = {
    'halt':0,
    'set':1,
    'push':2,
    'pop':3,
    'eq':4,
    'gt':5,
    'jmp':6,
    'jnz':7,
    'jz':8,
    'add':9,
    'mul':10,
    'mod':11,
    'and':12,
    'or':13,
    'not':14,
    'rmem':15,
    'wmem':16,
    'call':17,
    'ret':18,
    'out':19,
    'in':20,
    'nop':21
}

MNEUMONICS = dict((v,k) for k,v in OPCODES.items())
ARGCOUNT = array('B', [0,2,1,1,3,3,1,2,2,3,3,3,3,3,2,2,2,1,0,1,1,0])    

class Computer2:
    def __init__(self):
        self.emu = cEmulator();
        self.reset()


    def reset(self):
        dll.reset(byref(self.emu))

    def load_program_from_file(self, binfile):
            with open(binfile,'rb') as f:
                data = array('H')
                try:
                    data.fromfile(f,2**16)
                except EOFError:
                    pass

                program_len = len(data)
                program_data = (c_ushort * program_len)()
                for i,v in enumerate(data):
                    program_data[i] = v 
                dll.load(byref(self.emu),program_data,program_len)

    def run(self):
        dll.run(byref(self.emu))

    def __getattr__(self, name):
        if name in FIELDS:
            return getattr(self.emu, name)
        return super(Computer2, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in FIELDS:
            return setattr(self.emu,name,value)
        return super(Computer2,self).__setattr__(name,value)







class Computer:
    def __init__(self, debugging_mode = False):
        self.initialize()
        self.reset()
        
    def initialize(self):
        self.memory = array('H')#,[0] * 2**15)
        self.stored_memory = array('H')
        self.program_loaded = False
        self.breakpoints = array('H')

    def reset(self):
        self.memory = self.stored_memory
        self.at_breakpoint = False
        self.stack = array('H')
        self.call_stack = array('H')
        self.cycles = 0
        self.registers = array('H',[0] * 8)
        self.pc = 0
        self.halted = False
        self.input_buffer = ''
        self.output_buffer = ''
        self.waiting_for_input = False
    
    def AddBreakpoint(self, value):
        if value not in self.breakpoints:
            self.breakpoints.append(value)

    def ClearBreakpoints(self):
        self.breakpoints.clear()

    def RemoveBreakpoint(self, value):
        while value in self.breakpoints:
            self.breakpoints.remove(value)

    def __repr__(self):
        print("A computer", end = '')
        pass
    
  
    def value(self, arg):
        if arg >= 32768 and arg <= 32775:
            return self.registers[arg-32768]
        else:
            return arg

     
    def reg(val):
        return val - 32768
    
   
    def isreg(val):
        return val >= 32768 and val <= 32775


    def reg_or_value_string(val):
        if Computer.isreg(val):
            return 'r{}'.format(Computer.reg(val))
        else:
            return '{:04X}'.format(val)
    
    def load_program_from_file(self, binfile):
        with open(binfile,'rb') as f:
            try:
                self.stored_memory.fromfile(f,2**16)
                self.reset()
                self.program_loaded = True
            except EOFError:
                pass

    def load_program_from_data(self, data):
        self.stored_memory = data
        self.reset()
        self.program_loaded = True

    def is_opcode(opcode):
        return opcode >= 0 and opcode < len(mnemonic)


  
    def do_halt(self, args):
        self.halted = True

    def do_set(self, args):
        self.registers[Computer.reg(args[0])] = self.value(args[1])

    def do_push(self, args):
        self.stack.append(self.value(args[0]))

    def do_pop(self, args):
        self.registers[Computer.reg(args[0])] = self.stack.pop()

    def do_eq(self, args):
        if self.value(args[1]) == self.value(args[2]):
            self.registers[Computer.reg(args[0])] = 1
        else:
            self.registers[Computer.reg(args[0])] = 0

    def do_gt(self, args):
        self.registers[Computer.reg(args[0])] = int(self.value(args[1]) > self.value(args[2]))

    def do_jmp(self, args):
        self.pc = self.value(args[0])

    def do_jt(self, args):
        if self.value(args[0]) != 0:
                self.pc = self.value(args[1])

    def do_jf(self,args):
        if self.value(args[0]) == 0:
                self.pc = self.value(args[1])

    def do_add(self, args):
        self.registers[Computer.reg(args[0])] = (self.value(args[1]) + self.value(args[2])) % 32768

    def do_mult(self, args):
        self.registers[Computer.reg(args[0])] = (self.value(args[1]) * self.value(args[2])) % 32768

    def do_mod(self, args):
        self.registers[Computer.reg(args[0])] = (self.value(args[1]) % self.value(args[2])) % 32768

    def do_and(self, args):
        self.registers[Computer.reg(args[0])] = (self.value(args[1]) & self.value(args[2])) % 32768

    def do_or(self, args):
        self.registers[Computer.reg(args[0])] = (self.value(args[1]) | self.value(args[2])) % 32768    

    def do_not(self, args):
        self.registers[Computer.reg(args[0])] = (~self.value(args[1])) % 32768

    def do_rmem(self, args):
        self.registers[Computer.reg(args[0])] = self.memory[self.value(args[1])]

    def do_wmem(self, args):
        self.memory[self.value(args[0])] = self.value(args[1])

    def do_call(self, args):
        self.stack.append(self.pc)
        self.pc = self.value(args[0])
        self.call_stack.append(self.pc)

    def do_ret(self, args):
        self.pc = self.stack.pop()
        _ = self.call_stack.pop()


    def do_out(self, args):
        self.output_buffer += chr(self.value(args[0]))

    def do_in(self, args):
        if self.input_buffer == '':
            self.cycles -= 1
            self.waiting_for_input = True
            self.pc = self.pc - 2
            return
        self.waiting_for_input = False
        self.registers[Computer.reg(args[0])] = ord(self.input_buffer[0])
        self.input_buffer = self.input_buffer[1:]

    def do_nop(self, args):
        pass


    FCN_MAP = [do_halt, do_set, do_push, do_pop, do_eq, 
               do_gt, do_jmp, do_jt, do_jf, do_add, do_mult,
               do_mod, do_and, do_or, do_not, do_rmem,
               do_wmem, do_call, do_ret, do_out, do_in,
               do_nop
              ]

  
    def process_instruction(self):
        try:
            op = self.memory[self.pc]
            start = self.pc
            self.pc += (1 + ARGCOUNT[op])
            self.cycles += 1

            if op < len(Computer.FCN_MAP):
                Computer.FCN_MAP[op](self, self.memory[start+1:self.pc])
            else:
                print("Unknown opcode (0x{:02X}) @ 0x{:04X}".format(op,self.pc))
                self.halted = True
        except:
            self.halted = True
            return



    
    def run(self):
        while not self.halted:
            yield self.pc
            self.process_instruction()

    
    def run_until_done(self):
        while not self.halted and not self.waiting_for_input:
            self.process_instruction()

    
    def run_n_times(self, n, stop_at_breakpoints = False):
        self.at_breakpoint = False
        for _ in range(n):
            self.process_instruction()
            if stop_at_breakpoints and self.pc in self.breakpoints:
                self.at_breakpoint = True
                return
            if self.waiting_for_input:
                return
            if self.halted:
                return


    def Dump(self):
        filename = 'VM Dump {}.dump'.format(time.strftime("%Y%m%d-%H%M%S"))
        with open(filename, 'w') as f:
            f.write("pc: {:04x}\n".format(self.pc))
            for i in range(8):
                f.write("r{}: {:04x}\n".format(i,self.registers[i]))
            for i, v in enumerate(self.stack):
                f.write("stack({}): {:04X} ({})\n".format(i,v,self.stack_type[i]))
            f.write("Memory\n")
            for i in range(0,len(self.memory),16):
                chars = [['.',chr(x)][x>=ord(' ') and x <= ord('~')] for x in self.memory[i:i+16]]
                mem_string = ' '.join(["{:04X}".format(x) for x in self.memory[i:i+16]])
                char_string = ''.join(["{}".format(x) for x in chars])
                f.write("{:06X} | {} | {}\n".format(i,mem_string,char_string))

    def Print(self):
        print("pc: {:04x}".format(self.pc))
        for i in range(8):
            print("r{}: {:04x}".format(i,self.registers[i]))
        for i, v in enumerate(self.stack):
            print("stack({}): {:04X} ({})".format(i,v,self.stack_type[i]))
            

    # tests if the instruction is a valid format, this will prevent the DB seciont from
    # getting disassembled as strange instructions
    def valid_instruction(op_args):
        if op_args[0] >= 0 and op_args[0] <= 22:
            op = op_args[0]
            args = op_args[1:]
            
            if len(args) != ARGCOUNT[op]:
                return False
            
            if op == 0:
                return True
            elif op == 1: #set
                return Computer.isreg(args[0]) and args[1] < 32776
            elif op == 2: #push
                return args[0] < 32776
            elif op == 3: #pop
                return Computer.isreg(args[0])
            elif op == 4: #eq
                return Computer.isreg(args[0]) and args[1] < 32776 and args[2] < 32776
            elif op == 5: #gt
                return Computer.isreg(args[0]) and args[1] < 32776 and args[2] < 32776
            elif op == 6: #jmp
                return args[0] < 32776
            elif op == 7: #jt
                return args[0] < 32776 and args[1] < 32776
            elif op == 8: #jf
                return args[0] < 32776 and args[1] < 32776
            elif op == 9 or op == 10 or op == 11 or op == 12 or op == 13: #add, mult, mod, and, or
                return Computer.isreg(args[0]) and args[1] < 32776 and args[2] < 32776
            elif op == 14: #not
                return Computer.isreg(args[0]) and args[1] < 32776
            elif op == 15: #rmem
                return Computer.isreg(args[0]) and args[1] < 32776
            elif op == 16: #wmem
                return args[0] < 32776 and args[1] < 32776
            elif op == 17: #call
                return args[0] < 32776
            elif op == 18: #ret
                return True
            elif op == 19: #out
                return args[0] < 32776
            elif op == 20: #in
                return Computer.isreg(args[0])
            elif op == 21: #nop
                return True
            else:
                return False #no reach
        else:
            return False
        return False #no reach
        

    def DisassembleFile(program_file, verbose = False):
    
    # 00HHHH  |  HHHH HHHH HHHH HHHH  |  asm__opa, opb, opc 

        with open(program_file,'rb') as f:            
            data  = array('H')
            try:
                data.fromfile(f,2**16)
            except EOFError:
                pass
            return Computer.Disassemble(data,verbose)
        return []

    def Disassemble(data, verbose = False):
        disassembly = OrderedDict()
        file_size = len(data)
        addr = 0
        labels = {0:'init'}
        while addr < file_size:
            token = dict()
            token['start_address'] = addr
        
            if token['start_address'] in labels:
                token['label'] = labels[token['start_address']]
                del(labels[token['start_address']])
            else:
                token['label'] = ''            

            if data[addr] in MNEUMONICS and Computer.valid_instruction(data[addr:1+addr+ARGCOUNT[data[addr]]]):
                
                actual_values = data[addr:1+addr+ARGCOUNT[data[addr]]]
                addr += len(actual_values)

                token['op'] = MNEUMONICS[actual_values[0]]
                
                token['args'] = actual_values[1:]
                token['raw'] = actual_values
                token['size'] = len(actual_values)
                token['processed_args'] = []
                token['comment'] = ''

                for arg in token['args']:
                    token['processed_args'] += [Computer.reg_or_value_string(arg)]

                def update_label(addr, prefix, token, offset):
                    if token['start_address'] < addr:
                        labels[addr] = "{}_{:04X}".format(prefix,addr)
                        token['processed_args'][offset] = ".{}_{:04X}".format(prefix,addr)
                    elif addr in disassembly and disassembly[addr]['label'] == '':
                        disassembly[addr]['label'] = "{}_{:04X}".format(prefix,addr)
                        token['processed_args'][offset] = ".{}_{:04X}".format(prefix,addr)
                    elif addr not in disassembly:
                        pass
                    else:
                        token['processed_args'][offset] = "." + disassembly[addr]['label']

                if token['op'] == 'jmp' and not Computer.isreg(actual_values[1]):
                    update_label(actual_values[1],'jmp',token, 0)
                elif (token['op'] == 'jnz' or token['op'] == 'jz' ) and not Computer.isreg(actual_values[2]):
                    update_label(actual_values[2],'jmp',token, 1)
                elif token['op'] == 'call' and not Computer.isreg(actual_values[1]):
                    update_label(actual_values[1],'sub',token, 0)
                elif token['op'] == 'rmem' and not Computer.isreg(actual_values[2]):
                    update_label(actual_values[2],'mem',token, 1)
                elif token['op'] == 'wmem' and not Computer.isreg(actual_values[1]):
                    update_label(actual_values[1],'mem',token, 0)
                elif token['op'] == 'out' and actual_values[1] < 255:
                    if actual_values[1] == 10:
                        token['processed_args'][0] = r"'\n'"
                    else:
                        token['processed_args'][0] = r"'{}'".format(chr(actual_values[1]))


                #check valid
                if Computer.valid_instruction(actual_values):
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
                token['processed_args'] = ['{:04x}'.format(actual_values[0])]
                token['comment'] = ''
                disassembly[token['start_address']] = token
        return disassembly



    def Tokenize(line):
        parsed = dict()
        parsed['breakpoint'] = False
        parsed['address'] = None
        parsed['label'] = None
        parsed['instruction'] = None
        parsed['args'] = []
        parsed['comment'] = None
        parsed['size'] = 0

        

        make_tokens = re.compile(r'''\;[\w\s\-]*$|[\w]+\:|[\w\+\-\.]+|\'.+\'|\'\\n\'|@[0-9a-fA-F]{4}|^>''',re.VERBOSE).findall
        tokens = make_tokens(line)



        if tokens and tokens[0] == '>':
            parsed['breakpoint'] = True
            tokens = tokens[1:]

        if tokens and tokens[0].startswith('@'):
            parsed['address'] = int(tokens[0][1:],16)
            tokens = tokens[1:]

        if tokens and tokens[0].endswith(':'):
            parsed['label'] = tokens[0][:-1].lstrip()
            tokens = tokens[1:]

        if tokens and tokens[0] == 'db':
            parsed['instruction'] = tokens[0]
            tokens = tokens[1:]
            if len(tokens)>=1:
                parsed['args'] = [tokens[0]]
            else:
                print("Error: Insufficient arguments for operation"+parsed['instruction'])
            parsed['size'] = 1
        elif tokens and tokens[0] in OPCODES:
            parsed['instruction'] = tokens[0]
            tokens = tokens[1:]
            
            if len(tokens) >= ARGCOUNT[OPCODES[parsed['instruction']]]:
                parsed['args'] = [tokens[x] for x in range(ARGCOUNT[OPCODES[parsed['instruction']]])]
                parsed['size'] = 1 + ARGCOUNT[OPCODES[parsed['instruction']]]    
            else:
                print("Error: Insufficient arguments for operation"+parsed['instruction'])
        elif tokens and tokens[0].startswith(';'):
            pass
        elif not line or parsed['label']:
            pass
        else:
            print("Failed to tokenize:",line)
            print(line.split())
            print(tokens)
            exit()

        return parsed

    def AssembleLine(tokens, labels): #takes a token and converts to a string of bytes
        #returns {'label' : '', 'code':[1,2,3,4] }
        assembled_bytes = array('H')
        if tokens['instruction'] in OPCODES:
            assembled_bytes.append(OPCODES[tokens['instruction']])
        
        
        registers = ['r0','r1','r2','r3','r4','r5','r6','r7']
        for tok in tokens['args']:
            if tok in registers:
                assembled_bytes.append(2**15 + registers.index(tok))
            elif tok.startswith('.'):
                addition = 0
                if '+' in tok:
                    thing = tok.split('+')    
                    label = thing[0].lstrip('.')
                    addition = int(thing[1],16)
                elif '-' in tok:
                    thing = tok.split('-')    
                    label = thing[0].lstrip('.')
                    addition = -int(thing[1],16)
                else:
                    label = tok.lstrip('.')
                
                if label in labels:
                    assembled_bytes.append(labels[label] + addition)
                else:
                    print(label)
                    print(labels)
                    print("failed to assemble:",tokens)
                    assembled_bytes.append(0)
                    exit()
            elif tok == "'": #work around bug, the parsers pulls the space on -> out ' '
                assembled_bytes.append(ord(' '))
            elif tok == "'\\n'": #work around bug, the parsers pulls the space on -> out ' '
                assembled_bytes.append(ord('\n'))  
            elif tok.startswith("'") and tok.endswith("'"):
                assembled_bytes.append(ord(tok.strip("'"))) 
            else:
                assembled_bytes.append(int(tok,16) % (2**15))   
    
        return assembled_bytes
    
    def AssembleFile(filename, debug = False):
        with open(filename) as f:
            asm_lines = f.read().splitlines()
            breakpoints = array('H',[0])
            tokenized_lines = []
            current_address = 0
            current_offset = 0
            labels = dict()
            for asm_line in asm_lines:
                
                tl = Computer.Tokenize(asm_line.lstrip().rstrip())
                if tl:
                    if tl['address']:
                        current_offset = tl['address']
                        current_address = 0

                    if tl['label']:
                        labels[tl['label']] = current_address + current_offset
                    
                    if tl['breakpoint']:
                        breakpoints.append(current_address + current_offset)

                    tokenized_lines += [tl]
                    current_address += tl['size']    
            

            
            binary_data = array('H')
            for tok_line in tokenized_lines:
                #print('len:',len(binary_data),'tokenizing:',tok_line)
                
                if tok_line['address']:
                    fill_to = tok_line['address']
                    if fill_to < len(binary_data):
                        print("Can't achieve positional statement",tok_line,'size',len(binary_data))
                        print(tokenized_lines[:5])
                        exit()
                    if fill_to == len(binary_data):
                        pass
                    else:
                        binary_data += array('H',[21] * (fill_to - len(binary_data)))
                        #binary_data += [21] * (fill_to - len(binary_data))

                binary_data += Computer.AssembleLine(tok_line,labels)


            return (binary_data,breakpoints)