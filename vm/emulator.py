''' Emulator '''
from array import array

from ctypes import *
import os

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
