
# coding: utf-8

# # Synacor Challenge - Collect all 8 Codes...
# This probable has to move to an actual console window in order to make the debugger

# In[1]:

import sys

from pathlib import Path
from array import array

import time
import wx

from vm import AssembleFile, VirtualMachine, DisassembleFile, PrettyFile, ParseFile, Benchmark, SynacorWorkspace

def doui():
    app = wx.App()
    SynacorWorkspace(None, title="Synacor VM")
    app.MainLoop()


if __name__ == '__main__':

    if len(sys.argv) == 3 and sys.argv[1] == 'disassemble':
        disassembly = DisassembleFile(sys.argv[2])
        last_skipped = False

        for _,x in disassembly.items():
            if x['op'] == 'nop' and x['label'] == '':
                if last_skipped:
                    continue
                else:
                    last_skipped = True
                    print('\n                     ; -- nop --\n')
                    continue

            last_skipped = False
            if x['label'] != '':
                print('0x{:04X}  {:>12}  {:6} {}'.format(x['start_address'],x['label']+':',x['op'],' '.join(x['processed_args'])))
            else:
                print('0x{:04X}  {:>12}  {:6} {}'.format(x['start_address'],'',x['op'],' '.join(x['processed_args'])))


    elif len(sys.argv) == 4 and sys.argv[1] == 'assemble':
        input_file = Path(sys.argv[2])
        output_file = Path(sys.argv[3])


        bindata = AssembleFile(input_file) 
        with output_file.open('wb') as f:
            bindata.tofile(f)

    elif len(sys.argv) == 2 and sys.argv[1] == 'benchmark':
        Benchmark('programs/conway_life.asm', 10.0, 1000000)

    elif len(sys.argv) == 3 and sys.argv[1] == 'run':
        
        sys.stdout.write(" [ ] Creating Virtual Machine...")
        sys.stdout.flush()
        c = VirtualMachine()
        sys.stdout.write("\r [+] Virtual Machine Created...\n")
        sys.stdout.flush()
        sys.stdout.write(" [ ] Assembling File...")
        sys.stdout.flush()
        program = AssembleFile(sys.argv[2])
        sys.stdout.write("\r [+] File Assembled...   \n")
        sys.stdout.flush()
        sys.stdout.write(" [ ] Loading Binary Data...")
        sys.stdout.flush()
        c.LoadProgramFromData(program)
        sys.stdout.write("\r [+] Binary Data Loaded...   \n")
        sys.stdout.flush()
        print(' [*] Running Program!')
        print('*' * 80 + '\n')
        while not c.halted:
            c.Run()
            print(c.Output)
            c.Output = ''
            if c.waiting_for_input:
                c.Input = input() + '\n'
    else:
        doui()
        




    
