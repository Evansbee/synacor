''' WX Widgets & Customizations to make the UI for the Synacor Emulator'''

import wx
import wx.grid as gridlib
import wx.stc as stc
from wx.stc import StyledTextCtrl
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

class RegisterView(gridlib.Grid):
    def __init__(self, parent,  vm):
        gridlib.Grid.__init__(self, parent)
        self.vm = vm
        self.SetTable(RegisterData(self.vm),True)
        for i in range(9):

            self.SetColSize(i,60)



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


class MemoryView(gridlib.Grid):
    def __init__(self, parent,  vm):
        gridlib.Grid.__init__(self, parent)
        self.vm = vm
        self.SetTable(MemoryData(self.vm),True)
        for i in range(16):
            self.SetColSize(i,60)

class Editor(StyledTextCtrl):
    def __init__(self, parent, ID, vm):
        self.breakpoint_lines = []
        StyledTextCtrl.__init__(self,parent, ID)
        self.SetKeyWords(0, "nop set halt add eq mod push pop jnz gt jz jmp call in out")
        
        faces = { 'times': 'Times New Roman',
              'mono' : 'Consolas',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(mono)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default
    
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 40)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "size:%d,face:%s" % (10, 'mono'))


        self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        self.MarkerDefine(0, stc.STC_MARK_ROUNDRECT, "#CCFF00", "RED")

        self.SetMarginSensitive(1, True)

        self.Bind(stc.EVT_STC_MARGINCLICK, self.onSetRemoveBreakpoint)
    
    
    def GetLineFromPosition(self, pos):
        for i in range(self.GetLineCount()):
            line_end = self.GetLineEndPosition(i)
            if pos <= line_end:
                return i

    
    def onSetRemoveBreakpoint(self, e):
        line = self.GetLineFromPosition(e.GetPosition())
        if line in self.breakpoint_lines:
            self.GetParent().RemBreakpointAtLine(line)
            self.MarkerDelete(line,1)
            self.breakpoint_lines.remove(line)
        else:
            self.GetParent().AddBreakpointAtLine(line)
            self.MarkerAdd(line,1)
            self.breakpoint_lines.append(line)

    def HighlightLine(self,line):
        end = self.GetLineEndPosition(line)
        if line > 0:
            start = self.GetLineEndPosition(line - 1)
        else:
            start = 0
        self.SetSelection(start, end)


class SynacorWorkspace(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(SynacorWorkspace,self).__init__(*args,**kwargs)
        

        self.vm = VirtualMachine()
        self.current_program_status = 'Not Loaded'
        self.loaded_filename = None
        self.editor = Editor(self, -1, self.vm)


        self.mem_to_line = {}
        self.line_to_mem = {}

        self.output =  wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE | wx.TE_READONLY| wx.TE_RICH2)
        self.output.SetBackgroundColour( (0,0,0) )
        self.output.SetForegroundColour( (0xB0, 0xF0, 0xB0) )

        self.input = wx.TextCtrl(self, -1, "", style = wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_TEXT_ENTER, self.OnInput, self.input)
        self.setupTimers()

        self.register_map = RegisterView(self, self.vm)
        self.memory_map = MemoryView(self, self.vm)
        

        
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
        self.setupToolbar()
        self.setupMenuBar()
        self.setupTimers()
        self.setupStatusBar()
        self.Show()

    
    def setupStatusBar(self):
        self.status_bar = wx.StatusBar(self, -1)
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusText("Not Running", 0)
        self.status_bar.SetStatusText("0 Cycles", 1)
        self.SetStatusBar(self.status_bar)


    def setupToolbar(self):
        tsize = (24,24)

        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        compile_bmp = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, tsize)
        run_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, tsize)
        step_bmp = wx.ArtProvider.GetBitmap(wx.ART_GOTO_LAST, wx.ART_TOOLBAR, tsize)


        tb = self.CreateToolBar()
        opentool = tb.AddTool(wx.ID_ANY, 'Open', open_bmp)
        compiletool  = tb.AddTool(wx.ID_ANY, 'Compile', compile_bmp)
        runtool  = tb.AddTool(wx.ID_ANY, 'Run', run_bmp)
        steptool  = tb.AddTool(wx.ID_ANY, 'Step', step_bmp)

        tb.Realize()
        self.Bind(wx.EVT_TOOL, self.onLoad, opentool)
        self.Bind(wx.EVT_TOOL, self.onAssemble, compiletool)
        self.Bind(wx.EVT_TOOL, self.OnRunTool, runtool)
        self.Bind(wx.EVT_TOOL, self.onStep, steptool)
    

    def OnRunTool(self, e):
        self.editor.SetReadOnly(True)
        self.startProgramRun()

    def onAssemble(self, e):
        data, prog = Assemble(self.editor.GetValue())
        for line in prog.lines:
           #the line numbers coming in from the assembler are all fucked up, they're 1 based, the control is 0 based.
            if line.line_number > 0 and line.placement:
                self.line_to_mem[line.line_number-1] = line.placement
                self.mem_to_line[line.placement] = line.line_number-1
        self.vm.LoadProgramFromData(data)

    def onStep(self,e):
        self.Step()

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
        #self.Bind(wx.EVT_MENU, self.onRun, self.runButton)
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

    def updateUIElements(self):
        if not self.editor.GetLineVisible(self.mem_to_line[self.vm.pc]):
            self.editor.ScrollToLine(self.mem_to_line[self.vm.pc])
        self.editor.HighlightLine(self.mem_to_line[self.vm.pc])
        self.memory_map.ForceRefresh()
        self.register_map.ForceRefresh()
        if self.vm.halted:
            self.status_bar.SetStatusText("Halted", 0)
        if self.vm.at_breakpoint:
            self.status_bar.SetStatusText("Breakpoint", 0)
        if self.vm.waiting_for_input:
            self.status_bar.SetStatusText("Waiting for input", 0)

        self.status_bar.SetStatusText("{} Cycles".format(self.vm.cycles, 1))

    def Step(self):
        self.vm.RunNTimes(1)
        self.output.AppendText(self.vm.Output) 
        self.vm.Output = ""  
        self.updateUIElements()
        if self.vm.waiting_for_input:
            self.input.SetFocus()

    def AddBreakpointAtLine(self, line):
        print("adding breakpoint to line")
        self.vm.AddBreakpoint(self.line_to_mem[line])
    
    def RemBreakpointAtLine(self, line):
        self.vm.RemoveBreakpoint(self.line_to_mem[line])

    def runTick(self,e):
        self.vm.RunNTimes(100000)
        self.output.AppendText(self.vm.Output) 
        self.vm.Output = ""  
        if self.vm.halted:
            self.updateUIElements()
            self.runTimer.Stop()
        if self.vm.at_breakpoint:
            self.updateUIElements()
            self.runTimer.Stop()
        if self.vm.waiting_for_input:
            self.updateUIElements()
            self.runTimer.Stop()
            self.input.SetFocus()