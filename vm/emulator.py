''' Emulator '''
from array import array
from ctypes import *
import os

from .assembler import OPCODES, REGISTERS, MNEUMONICS, REV_REGISTERS, ARGCOUNT


dll = CDLL(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'bin', '_emu')))

class cEmulator(Structure):
    _fields_ = [
        ('pc', c_ushort),
        ('registers', c_ushort * 8),
        ('memory', c_ushort * 0x7FFF),
        ('stored_memory', c_ushort * 0x7FFF),
        ('breakpoints', c_ushort * 64),
        ('breakpoint_write_pointer',c_ushort),
        ('stack', c_ushort * 1000),
        ('stack_write_pointer', c_ushort),
        ('cycles',c_ulonglong),
        ('input_buffer',c_char * 2048),
        ('input_buffer_write_pointer',c_ushort),
        ('output_buffer',c_char * 2048),
        ('halted',c_int),
        ('program_loaded',c_int),
        ('waiting_for_input', c_int),
        ('output_buffer_full', c_int),
        ('stack_overflow', c_int),
        ('at_breakpoint', c_int),
        ('memory_read_history', c_ulong * 0x7FFF),
        ('memory_write_history', c_ulong * 0x7FFF),
    ]

FIELDS = set(x[0] for x in cEmulator._fields_)

class VirtualMachine(object):
    '''Virtual Synacore Machine'''
    def __init__(self):
        self.emu = cEmulator()    
        self.Output = ''
        self.Reset()

    def Reset(self):
        dll.reset(byref(self.emu))

    def AddBreakpoint(self, val):
        dll.add_breakpoint(byref(self.emu),val)

        
    def RemoveBreakpoint(self, val):
        dll.remove_breakpoint(byref(self.emu),val)

    def LoadProgramFromData(self, bindata):
        program_len = len(bindata)
        program_data = (c_ushort * program_len)()
        for i, val in enumerate(bindata):
            program_data[i] = val 
        dll.load(byref(self.emu),program_data,program_len) 


    def LoadProgramFromFile(self, binfile):
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

    def Run(self, supress_output = False):
        dll.run(byref(self.emu))
        self.Output += self.emu.output_buffer.decode('UTF-8')
        self.emu.output_buffer = ''.encode('UTF-8')
        if self.emu.waiting_for_input or self.emu.halted or self.emu.at_breakpoint:
            return

    def ClearMemoryHistory(self):
        dll.clear_memory_history(byref(self.emu))

    def RunNTimes(self, times, supress_output = False):
        start_cycles = self.cycles
        while self.cycles < start_cycles + times:
            dll.run_n(byref(self.emu), start_cycles + times - self.cycles)
            
            self.Output += self.emu.output_buffer.decode('UTF-8')
            self.emu.output_buffer = ''.encode('UTF-8')
            
            if self.emu.waiting_for_input or self.emu.halted or self.emu.at_breakpoint:
                #print(f'{self.emu.waiting_for_input}{self.emu.halted}{self.emu.at_breakpoint}')
                return
            
    def __getattr__(self, name):
        if name in FIELDS:
            return getattr(self.emu, name)
        return super(VirtualMachine, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name == 'Input':
            #print("appending input buffer")
            current = self.emu.input_buffer.decode('UTF-8')
            current += value
            self.emu.input_buffer = current[:2047].encode('UTF-8')
        if name in FIELDS:
            return setattr(self.emu,name,value)
        return super(VirtualMachine,self).__setattr__(name,value)


class VirtualMachine2(object):
    def __init__(self):
        self.Registers = array('H',[0] * 8)
        self.PC = 0
        self.OutputBuffer = ""
        self.InputBuffer = ""
        self.Breakpoints = Set()
        self.Stack = array('H')
        self.StackItemType = []
        self.Memory = None
        self.StartingMemory = None
        self.Cycles = 0
        self.AtBreakpoint = False
        self.Halted = True
        self.WaitingForInput = False

    def Reset(self):
        self.Memory = self.StoredMemory
        self.Stack = array('H')
        self.StackItemType = []
        self.OutputBuffer = ""
        self.InputBuffer = ""
        self.PC = 0
        self.AtBreakpoint = False
        self.Halted = False
        self.WaitingForInput = False
        self.Cycles = 0

    #convenience
    def Step(self):
        self.Run(1)
    
    def RunForever(self):
        self.Run(-1)


    def Run(self, times = -1):
        run_count = 0
        while times > 0 and run_count < times:
            run_count += 1
            pass


    def _value(self, arg):
        if arg >= 32768 and arg <= 32775:
            return self.registers[arg-32768]
        else:
            return arg

    def _perform_instruction(self):
        op = self.memory[self.PC]
        try:
            args = array('H', [self.memory[self.PC + x + 1] for x in range(ARGCOUNT[op])])
        except IndexError:
            self.Halted = True
            return

        self.pc += (1 + ARGCOUNT[op])
        
        if op == 0: #halt
            self.Halted = True
        elif op == 1: #set
            self.Registers[Computer.reg(args[0])] = self.value(args[1])
        elif op == 2: #push
            self.stack += [self.value(args[0])]
        elif op == 3: #pop
            self.Registers[Computer.reg(args[0])] = self.stack.pop()
        elif op == 4: #eq
            self.Registers[Computer.reg(args[0])] = int(self.value(args[1]) == self.value(args[2]))
        elif op == 5: #gt
            self.Registers[Computer.reg(args[0])] = int(self.value(args[1]) > self.value(args[2]))
        elif op == 6: #jmp
            self.pc = self.value(args[0])
        elif op == 7: #jnz
            if self.value(args[0]) != 0:
                self.PC = self.value(args[1])
        elif op == 8: #jz
            if self.value(args[0]) == 0:
                self.PC = self.value(args[1])
        elif op == 9: #add
            self.Registers[Computer.reg(args[0])] = (self.value(args[1]) + self.value(args[2])) % 32768
        elif op == 10: #mult
            self.Registers[Computer.reg(args[0])] = (self.value(args[1]) * self.value(args[2])) % 32768
        elif op == 11: #mod
            self.Registers[Computer.reg(args[0])] = (self.value(args[1]) % self.value(args[2])) % 32768
        elif op == 12: #and
            self.Registers[Computer.reg(args[0])] = (self.value(args[1]) & self.value(args[2])) % 32768
        elif op == 13: #or
            self.Registers[Computer.reg(args[0])] = (self.value(args[1]) | self.value(args[2])) % 32768    
        elif op == 14: #not
            self.Registers[Computer.reg(args[0])] = (~self.value(args[1])) % 32768
        elif op == 15: #rmem
            self.Registers[Computer.reg(args[0])] = self.memory[self.value(args[1])]
        elif op == 16: #wmem
            self.memory[self.value(args[0])] = self.value(args[1])
        elif op == 17: #call
            self.stack += [self.pc]
            self.PC = self.value(args[0])
        elif op == 18: #ret
            self.PC = self.stack.pop()
        elif op == 19: #out
            self.OutputBuffer += chr(self.value(args[0]))
        elif op == 20: #in
            if self.InputBuffer == '':
                self.WaitingForInput = True
                self.PC -= 2
                self.Cycles -= 1
                return 
            self.WaitingForInput = False
            self.registers[Computer.reg(args[0])] = ord(self.input_buffer[0])
            self.input_buffer = self.input_buffer[1:]
        elif op == 21: #nop
            pass
        else:
            print("Unknown opcode (0x{:02X}) @ 0x{:04X}".format(op,self.pc))
            self.running = False
        #does not use self.pc because you could want to pass in something 

    def LoadData(self, data):
        try:
            self.StartingMemory.fromfile(f,2**16)
        except EOFError:
            pass
        self.Reset()

    def AddBreakpoint(self, bp):
        pass

    def RemoveBreakpoint(self, bp):
        pass

    def SaveState(self, save_name):
        pass

    def LoadState(self, load_name):
        pass
















class Computer:
       
 
    
    
        
    def reg(val):
        return val - 32768
    
    def isreg(val):
        return val in REV_REGISTER

    def is_opcode(opcode):
        return opcode >= 0 and opcode < len(mnemonic)
    
    def process_instruction(self):
        op = self.memory[self.pc]
        try:
            args = array('H', [self.memory[self.pc + x + 1] for x in range(ARGCOUNT[op])])
        except IndexError:
            self.Halted = True
            return

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
        elif op == 7: #jnz
            if self.value(args[0]) != 0:
                self.pc = self.value(args[1])
        elif op == 8: #jz
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
            