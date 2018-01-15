from array import array
from collections import OrderedDict

OPCODES = {
    'halt':0,
    'set':1,
    'push':2,
    'pop':3,
    'eq':4,
    'gt':5,
    'jmp':6,
    'jt':7,
    'jf':8,
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


class Computer:
    def __init__(self, debugging_mode = False):
        self.reset()
        self.debugging = debugging_mode
        
    def assy_line(self, memory_address):
        return 0

    def get_assy_line(self, line_no):

        return self.assembly_cache[line_no]

    def reset(self):
        self.assembly_cache = []
        self.memory_to_assembly = []

        self.memory = array('H')#,[0] * 2**15)
        self.stack = []
        self.call_stack = []
        self.cycles = 0
        self.registers = array('H',[0] * 8)
        self.pc = 0
        self.running = False
        self.breakpoints = dict()
        self.input_buffer = ''
        self.output_buffer = ''
    
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
            return 'r{}  '.format(Computer.reg(val))
        else:
            return '{:04X}'.format(val)
    
    def load_program_from_file(self, binfile):
        with open(binfile,'rb') as f:
            try:
                self.memory.fromfile(f,2**16)
            except EOFError:
                pass
            if self.debugging:
                self.pre_process_image()

    def load_program_from_data(self, data):
        self.memory = data
        if self.debugging:
            self.pre_process_image()
      
    def pre_process_image(self):
        self.assembly_cache = []
        self.memory_to_assembly = []
    

    def is_opcode(opcode):
        return opcode >= 0 and opcode < len(mnemonic)

    def arg_count_for_opcode(opcode):
        return ARGCOUNT[opcode]
    
    def process_instruction(self):
        op = self.memory[self.pc]
        try:
            args = array('H', [self.memory[self.pc + x + 1] for x in range(ARGCOUNT[op])])
        except IndexError:
            print("PC:",self.pc)
            print("OP:",op)
            print("FUCKED")
            exit()
        self.pc += (1 + ARGCOUNT[op])
        
        if op == 0: #halt
            self.running = False
        elif op == 1: #set
            self.registers[Computer.reg(args[0])] = self.value(args[1])
        elif op == 2: #push
            self.stack += [self.value(args[0])]
        elif op == 3: #pop
            self.registers[Computer.reg(args[0])] = self.stack.pop()
        elif op == 4: #eq
            self.registers[Computer.reg(args[0])] = int(self.value(args[1]) == self.value(args[2]))
        elif op == 5: #gt
            self.registers[Computer.reg(args[0])] = int(self.value(args[1]) > self.value(args[2]))
        elif op == 6: #jmp
            self.pc = self.value(args[0])
        elif op == 7: #jt
            if self.value(args[0]) != 0:
                self.pc = self.value(args[1])
        elif op == 8: #jf
            if self.value(args[0]) == 0:
                self.pc = self.value(args[1])
        elif op == 9: #add
            self.registers[Computer.reg(args[0])] = (self.value(args[1]) + self.value(args[2])) % 32768
        elif op == 10: #mult
            self.registers[Computer.reg(args[0])] = (self.value(args[1]) * self.value(args[2])) % 32768
        elif op == 11: #mod
            self.registers[Computer.reg(args[0])] = (self.value(args[1]) % self.value(args[2])) % 32768
        elif op == 12: #and
            self.registers[Computer.reg(args[0])] = (self.value(args[1]) & self.value(args[2])) % 32768
        elif op == 13: #or
            self.registers[Computer.reg(args[0])] = (self.value(args[1]) | self.value(args[2])) % 32768    
        elif op == 14: #not
            self.registers[Computer.reg(args[0])] = (~self.value(args[1])) % 32768
        elif op == 15: #rmem
            self.registers[Computer.reg(args[0])] = self.memory[self.value(args[1])]
        elif op == 16: #wmem
            self.memory[self.value(args[0])] = self.value(args[1])
        elif op == 17: #call
            self.stack += [self.pc]
            self.pc = self.value(args[0])
        elif op == 18: #ret
            self.pc = self.stack.pop()
        elif op == 19: #out
            self.output_buffer += chr(self.value(args[0]))
        elif op == 20: #in
            if self.input_buffer == '':
                self.input_buffer = input() + '\n'
            self.registers[Computer.reg(args[0])] = ord(self.input_buffer[0])
            self.input_buffer = self.input_buffer[1:]
        elif op == 21: #nop
            pass
        else:
            print("Unknown opcode (0x{:02X}) @ 0x{:04X}".format(op,self.pc))
            self.running = False
        #does not use self.pc because you could want to pass in something 
    
    def run(self):
        self.running = True
        
        while self.running:
            yield self.pc
            self.process_instruction()
            
    def get_instruction_at(self, address):
        op = self.memory[address]
        if op <= 21:
            args = array('H', [op] + [self.memory[address + 1 + x] for x in range(ARGCOUNT[op])])
            if Computer.valid_instruction(args):
                return args
        return None
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
                
                actual_values = [data[addr]]
                addr += 1
                token['op'] = MNEUMONICS[actual_values[0]]
                for _ in range(ARGCOUNT[actual_values[0]]):
                    actual_values += [data[addr]]
                    addr += 1
            

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
                elif (token['op'] == 'jt' or token['op'] == 'jf' ) and not Computer.isreg(actual_values[2]):
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
