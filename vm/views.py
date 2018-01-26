import wx

from .assembler import Assemble, Disassemble, Pretty, Parse
from .emulator import VirtualMachine



class SynacorWorkspace(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(SynacorWorkspace,self).__init__(*args,**kwargs)
        self.vm = VirtualMachine()
        self.current_program_status = 'Not Loaded'

        self.loaded_filename = None


        self.editor = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE | wx.TE_RICH2)

        self.output =  wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE | wx.TE_READONLY| wx.TE_RICH2)
        self.output.SetBackgroundColour( (0,0,0) )
        self.output.SetForegroundColour( (0xB0, 0xF0, 0xB0) )

        self.input = wx.TextCtrl(self, -1, "", style = wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_TEXT_ENTER, self.OnInput, self.input)
        self.setupTimers()

        
        rightPane = wx.BoxSizer(wx.VERTICAL)
        leftPane = wx.BoxSizer(wx.VERTICAL)

        leftPane.Add(self.editor,1,wx.EXPAND|wx.ALL,5)
        leftPane.Add(self.output,1,wx.EXPAND|wx.ALL, 5)
        leftPane.Add(self.input,0,wx.EXPAND|wx.ALL, 5)



        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(leftPane, 1, wx.EXPAND | wx.ALL, 5)
        layout.Add(rightPane, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(layout)
        self.SetAutoLayout(True)
        self.setupMenuBar()
        self.setupTimers()
        self.Show()


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
        with wx.FileDialog(self, 'Open Binary File', wildcard="*.asm",style = wx.FD_OPEN | wx. FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            try:
                with open(fileDialog.GetPath(), 'r') as f:
                    self.editor.SetValue(f.read())
                #self.computer.load_program_from_file(fileDialog.GetPath())
                self.runButton.Enable(True)
                #self.stopButton.Enable(True)
                #self.pauseButton.Enable(True)
                #self.stepIntoButton.Enable(True)
                #self.stepOverButton.Enable(True)
            except:
                print('Error')

    def onRun(self, e):
        data = Assemble(self.editor.GetValue())
        self.vm.LoadProgramFromData(data)
        #TODO FIND A WAY TO POP A DIALOG FOR THIS.
        self.startProgramRun()

    def onQuit(self, e):
        self.Close()


    def OnInput(self, e):
        self.vm.Input = self.input.GetValue() + '\n'
        self.output.AppendText(self.input.GetValue() + '\n') 
        self.input.SetValue('')
        if self.vm.waiting_for_input:
            self.startProgramRun()

    def setupTimers(self):
        self.runTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.runTick)
    
    def startProgramRun(self):
        self.runTimer.Start(100)        

    def onClearMemoryHistory(self, e):
        pass

    def updateMemoryGrid(self):
        pass

    def updateRegisters(self):
        pass


    def runTick(self,e):
        self.vm.RunNTimes(100000)
        self.output.AppendText(self.vm.Output) 
        self.vm.Output = ""  
        if self.vm.halted:
            self.runTimer.Stop()
        if self.vm.at_breakpoint:
            self.runTimer.Stop()
        if self.vm.waiting_for_input:
            self.runTimer.Stop()
            self.input.SetFocus()