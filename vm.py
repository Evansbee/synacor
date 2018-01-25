
# coding: utf-8

# # Synacor Challenge - Collect all 8 Codes...
# This probable has to move to an actual console window in order to make the debugger

# In[1]:

import sys

from pathlib import Path
from array import array
import wx
import time

from vm import AssembleFile, VirtualMachine, DisassembleFile, PrettyFile, ParseFile, Benchmark

class emuWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(emuWindow,self).__init__(*args,**kwargs)
        self.computer = Computer()
        self.setupMenuBar()
        self.setupButtonPanel()
        self.setupOutputPanel()
        self.setupMemoryPanel()
        self.setupRegistersPanel()
        self.setupCodePanel()
        self.setupBreakpointPanel()
        self.setupInputPanel()
        self.setupTimers()
        self.runCount = 0
        self.Show()


    def setupTimers(self):
        self.runTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.runTick)

    def startProgramRun(self):
        self.runTimer.Start(100)        

    def runTick(self,e):
        self.computer.run_n_times(100000)

        if self.computer.output_buffer != '':
            print(self.computer.output_buffer)
            self.computer.output_buffer = ''
        
        if self.computer.halted:
            self.runTimer.Stop()
            print("Halted")
        if self.computer.at_breakpoint:
            self.runTimer.Stop()
            print("Breakpoint")
        if self.computer.waiting_for_input:
            self.runTimer.Stop()
            print("Waiting For Input")


    def setupInputPanel(self):
        panel = wx.Panel(self)
        self.inputBox = wx.TextCtrl(panel, style = wx.TE_PROCESS_ENTER, pos=(10,10),size=(250,150))
        self.Bind(wx.EVT_TEXT_ENTER, self.onInputTextEnter)
        
    def onInputTextEnter(self, e):
        if self.computer.waiting_for_input:
            self.computer.input_buffer = self.inputBox.GetValue() + '\n'
            self.startProgramRun()
        self.inputBox.SetValue('')

    def setupButtonPanel(self):
        pass

    def setupOutputPanel(self):
        pass

    def setupMemoryPanel(self):
        pass

    def setupRegistersPanel(self):
        pass

    def setupCodePanel(self):
        pass

    def setupBreakpointPanel(self):
        pass


    def updateDisplay(self):
        pass


    def setupMenuBar(self):
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        openButton = fileMenu.Append(wx.ID_OPEN,'Open Program','')
        quitButton = fileMenu.Append(wx.ID_EXIT,'Quit','')


        runMenu = wx.Menu()
        self.runButton = runMenu.Append(wx.ID_ANY, 'Run Program')
        self.stopButton = runMenu.Append(wx.ID_ANY, 'Stop Program')
        self.pauseButton = runMenu.Append(wx.ID_ANY, 'Pause Program')
        self.stepIntoButton = runMenu.Append(wx.ID_ANY, 'Step Into')
        self.stepOverButton = runMenu.Append(wx.ID_ANY, 'Step Over')

        self.runButton.Enable(False)
        self.stopButton.Enable(False)
        self.pauseButton.Enable(False)
        self.stepIntoButton.Enable(False)
        self.stepOverButton.Enable(False)

        breakMenu = wx.Menu()
        clearButton = breakMenu.Append(wx.ID_ANY, 'Clear Breakpoints')



        menuBar.Append(fileMenu,'File')
        menuBar.Append(runMenu,'Run')
        menuBar.Append(breakMenu,'Breakpoints')

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onRun, self.runButton)
        self.Bind(wx.EVT_MENU, self.onQuit, quitButton)
        self.Bind(wx.EVT_MENU, self.onLoad, openButton)
        self.Title = 'Synacor VM'

    def onLoad(self, e):
        with wx.FileDialog(self, 'Open Binary File', wildcard="*.bin",style = wx.FD_OPEN | wx. FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            try:
                self.computer.load_program_from_file(fileDialog.GetPath())
                self.runButton.Enable(True)
                self.stopButton.Enable(True)
                self.pauseButton.Enable(True)
                self.stepIntoButton.Enable(True)
                self.stepOverButton.Enable(True)
            except:
                print('Error')

        
        
    def onRun(self, e):
        self.startProgramRun()
        print('running')

    def onQuit(self, e):
        print('quit')
        self.Close()
        

def doui():
    app = wx.App()
    emuWindow(None, title="Synacor VM")
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
        




    
