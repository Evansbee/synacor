
# coding: utf-8

# # Synacor Challenge - Collect all 8 Codes...
# This probable has to move to an actual console window in order to make the debugger

# In[1]:

import sys
from computer import Computer


   


if __name__ == '__main__':
    #dis = disassemble('docs/challenge.bin', True)
    #with open('docs/challenge-details-clean.out','w') as f:
    #   f.write('\n'.join(dis))
    
    print('usage:')
    print('{} disassemble [binary input] [asm output]'.format(sys.argv[0]))
    print('{} assemble [asm input] [binary output] <[breakpoint file]>'.format(sys.argv[0]))
    print('{} run [binary input] <[breakpoint file]>'.format(sys.argv[0]))

    if len(sys.argv) > 3 and sys.argv[1] == 'disassemble':
        disasm = Computer.DisassembleFile(sys.argv[2])
        with open(sys.argv[3], 'w') as f:
            for _,x in disasm.items():
                if x['label'] != '':
                    f.write('@{:04X}  {:>12}  {:6} {}\n'.format(x['start_address'],x['label']+':',x['op'],' '.join(x['processed_args'])))
                else:
                    f.write('@{:04X}  {:>12}  {:6} {}\n'.format(x['start_address'],'',x['op'],' '.join(x['processed_args'])))
    elif len(sys.argv) > 3 and sys.argv[1] == 'assemble':
        bindata, breakpoints = Computer.AssembleFile(sys.argv[2]) 
        print('breakpoints:',breakpoints)
        with open(sys.argv[3],'wb') as f:
            bindata.tofile(f)
    elif len(sys.argv) > 1:
        
        c = Computer()
        c.load_program_from_file(sys.argv[1])


        for next_address in c.run():
            if c.waiting_for_input:
                print(">",end=' ')
                buf = input()
                if buf == 'dump':
                    c.Dump()
                elif buf == 'quit':
                    c.Dump()
                    sys.exit()
                else:
                    c.input_buffer = buf + "\n"
            #sys.stdout.write('\r{:04X}'.format(next_address))
            #sys.stdout.flush()
            breakpoints = [0]
            if next_address in breakpoints:
                print("BREAK ({:04X})".format(next_address))
                print(">",end=' ')
                buf = input()
                if buf == 'dump':
                    c.Dump()
                elif buf == 'quit':
                    c.Dump()
                    sys.exit()
                else:
                    pass
            if c.output_buffer != '':
                print(c.output_buffer,end='')
                c.output_buffer = ''



    