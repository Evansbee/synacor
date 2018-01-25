from array import array
from collections import OrderedDict
import re
import datetime
import time
from ctypes import *
import os

dll = CDLL(os.path.realpath(os.path.join(os.path.dirname(__file__), 'bin', '_emu')))

class cEmulator(Structure):
    _fields_ = [
        ('pc', c_ushort),
        ('registers', c_ushort * 8),
        ('memory', c_ushort * 0x7FFF),
        ('breakpoints', c_ushort * 64),
        ('breakpoint_write_pointer',c_ushort),
        ('stack', c_ushort * 1000),
        ('stack_write_pointer', c_ushort),
        ('cycles',c_ulonglong),
        ('input_buffer',c_char * 2048),
        ('output_buffer',c_char * 2048),
        ('input_buffer_write_pointer',c_ushort),
        ('halted',c_int),
        ('program_loaded',c_int),
        ('waiting_for_input', c_int),
        ('output_buffer_full', c_int),
        ('stack_overflow', c_int),
        ('at_breakpoint', c_int),
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

MNEUMONICS = dict((v, k) for k, v in OPCODES.items())
ARGCOUNT = array('B', [0, 2, 1, 1, 3, 3, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0, 1, 1, 0])

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
        elif chr(val) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-=+_!@#$%^&*()[]{}\|;\':",.<>/?`~"':
            return "'" + chr(val) + "'"
        else:
            return '0x{:04X}'.format(val)
    
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
        
        

