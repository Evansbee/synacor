''' WX Widgets & Customizations to make the UI for the Synacor Emulator'''

import wx
import wx.grid as gridlib
from .assembler import Assemble, Disassemble, Pretty, Parse
from .emulator import VirtualMachine
import string

class RegisterData(gridlib.GridTableBase):
    def __init__(self, vm):
        gridlib.GridTableBase.__init__(self)
        self.vm = vm

    def GetNumberRows(self):
        return 1

    def GetNumberCols(self):
        return 9

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        if col < 8:
            if chr(self.vm.registers[col]) in string.printable:
                return "{:04X} ('{}')".format(self.vm.registers[col],chr(self.vm.registers[col]))
            return "{:04X}".format(self.vm.registers[col])
        else:
            return "{:04X}".format(self.vm.pc)

    def SetValue(self, row, col, value):
        try:
            value = int(value,16)
            if col < 8:
                self.vm.registers[col] = value
            else:
                self.vm.pc = value
        except:
            print("Error Setting Value")

    def GetColLabelValue(self, col):
        if col < 8:
            return 'r{}'.format(col)
        else:
            return 'pc'


    def GetRowLabelValue(self, row):
        return 'Registers'


class MemoryData(gridlib.GridTableBase):
    def __init__(self, vm):
        gridlib.GridTableBase.__init__(self)
        self.vm = vm
        self.changed = gridlib.GridCellAttr()
        self.changed.SetBackgroundColour(wx.RED)
        self.rw = gridlib.GridCellAttr()
        self.rw.SetBackgroundColour(wx.GREEN)
        self.pc = gridlib.GridCellAttr()
        self.pc.SetBackgroundColour(wx.BLUE)
        self.normal = gridlib.GridCellAttr()
        self.normal.SetBackgroundColour(wx.WHITE) 

    def GetNumberRows(self):
        return 0x7FFF//16

    def GetNumberCols(self):
        return 16

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        if chr(self.vm.memory[row*16 + col]) in string.printable:
            return "{:04X} ('{}')".format(self.vm.memory[row*16 + col],chr(self.vm.memory[row*16 + col]))
        return "{:04X}".format(self.vm.memory[row*16 + col])

    def SetValue(self, row, col, value):
        try:
            self.vm.memory[row*16 + col] = int(value,16)
        except:
            print("Error Setting Value")

    def GetColLabelValue(self, col):
        return '{:X}'.format(col)

    def GetRowLabelValue(self, row):
        return '{:04X}'.format(row*16)

    

    def GetAttr(self, row, col, kind):
        addr = row*16 + col
        attr = None
        
        if self.vm.pc == addr:
            attr =  self.pc
        elif self.vm.memory[addr] != self.vm.stored_memory[addr]:
            attr = self.changed
        elif self.vm.memory_read_history[addr] > 0:
            attr = self.rw
        else:
            attr = self.normal
        attr.IncRef()
        return attr


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

        self.register_map = gridlib.Grid(self)
        self.register_map.SetTable(RegisterData(self.vm),True)

        self.memory_map = gridlib.Grid(self)
        self.memory_map.SetTable(MemoryData(self.vm),True)
        
        #for i in range(0x7ffff//16 + 1):
        #    self.memory_map.SetRowLabelValue(i, '{:04X}'.format(i * 16))

        for i in range(9):
            self.register_map.SetColSize(i,50)

        for i in range(16):
            self.memory_map.SetColSize(i,60)
         #   self.memory_map.SetColLabelValue(i,'{:X}'.format(i))

        
        rightPane = wx.BoxSizer(wx.VERTICAL)

        rightPane.Add(self.register_map,1,wx.EXPAND | wx.ALL, 5)
        rightPane.Add(self.memory_map, 1, wx.EXPAND | wx.ALL, 5)

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
        #self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.onCellChange)
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
            self.vm.ClearMemoryHistory()
            self.startProgramRun()

    def setupTimers(self):
        self.runTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.runTick)
    
    def startProgramRun(self):
        self.runTimer.Start(100)        

    def onClearMemoryHistory(self, e):
        self.vm.ClearMemoryHistory()

    def runTick(self,e):
        self.vm.RunNTimes(100000)
        self.output.AppendText(self.vm.Output) 
        self.vm.Output = ""  
        if self.vm.halted:
            self.memory_map.ForceRefresh()
            self.register_map.ForceRefresh()
            self.runTimer.Stop()
        if self.vm.at_breakpoint:
            self.memory_map.ForceRefresh()
            self.register_map.ForceRefresh()
            self.runTimer.Stop()
        if self.vm.waiting_for_input:
            self.memory_map.ForceRefresh()
            self.register_map.ForceRefresh()
            self.runTimer.Stop()
            self.input.SetFocus()