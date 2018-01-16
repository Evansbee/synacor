
# coding: utf-8

# # Synacor Challenge - Collect all 8 Codes...
# This probable has to move to an actual console window in order to make the debugger

# In[1]:

import sys
from computer import Computer
from pathlib import Path
from array import array
import wx

#app = wx.App()
#frm = wx.Frame(None, title="Synacor VM")
#frm.Show()
#app.MainLoop()   


if __name__ == '__main__':

    print('usage:')
    print('{} disassemble [binary input] [asm output]'.format(sys.argv[0]))
    print('{} assemble [asm input] [binary output] <[breakpoint file]>'.format(sys.argv[0]))
    print('{} run [binary input]'.format(sys.argv[0]))

    if len(sys.argv) == 4 and sys.argv[1] == 'disassemble':
        input_file = Path(sys.argv[2])
        output_file = Path(sys.argv[3])
        
        disassembly = Computer.DisassembleFile(input_file)
        last_skipped = False
        with output_file.open('w') as f:
            for _,x in disassembly.items():
                if x['op'] == 'nop':
                    if last_skipped:
                        continue
                    else:
                        last_skipped = True
                        f.write('\n                     ; -- nop --\n\n')
                        continue

                last_skipped = False
                if x['label'] != '':
                    f.write('@{:04X}  {:>12}  {:6} {}\n'.format(x['start_address'],x['label']+':',x['op'],' '.join(x['processed_args'])))
                else:
                    f.write('@{:04X}  {:>12}  {:6} {}\n'.format(x['start_address'],'',x['op'],' '.join(x['processed_args'])))


    elif len(sys.argv) == 4 and sys.argv[1] == 'assemble':
        input_file = Path(sys.argv[2])
        output_file = Path(sys.argv[3])
        breakpoint_file = output_file.with_suffix('.bp')

        bindata, breakpoints = Computer.AssembleFile(input_file) 
        with output_file.open('wb') as f:
            bindata.tofile(f)

        with breakpoint_file.open('wb') as f:
            breakpoints.tofile(f)

    elif len(sys.argv) == 3 and sys.argv[1] == 'run':
        input_file = Path(sys.argv[2])
        breakpoint_file = input_file.with_suffix('.bp')
        
        c = Computer()
        c.load_program_from_file(sys.argv[2])

        breakpoints = array('H')

        try:
            with breakpoint_file.open('rb') as f:
                try:
                    breakpoints.fromfile(f,1000)
                except:
                    pass
        except:
            print('Failed to open:',breakpoint_file)

        print('Breakpoints: ',breakpoints)
        for next_address in c.run():
            if c.waiting_for_input:
                print(">",end=' ')
                buf = input()
                if buf == 'dump':
                    c.Dump()
                elif buf == 'quit':
                    c.Dump()
                    sys.exit()
                elif buf == 'print':
                    c.Print()
                else:
                    c.input_buffer = buf + "\n"
            #sys.stdout.write('\r{:04X}'.format(next_address))
            #sys.stdout.flush()
            
            if next_address in breakpoints:
                print("BREAK ({:04X})".format(next_address))
                print(">",end=' ')
                buf = input()
                if buf == 'dump':
                    c.Dump()
                elif buf == 'quit':
                    c.Dump()
                    sys.exit()
                elif buf == 'print':
                    c.Print()
                else:
                    pass
            if c.output_buffer != '':
                print(c.output_buffer,end='')
                c.output_buffer = ''



    