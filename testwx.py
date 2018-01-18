import wx

class DebuggerList(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        super(DebuggerList, self).__init__(style = wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_SINGLE_SEL, *args, **kwargs)

class Emulator(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Emulator, self).__init__(*args,**kwargs)
        self.InitUI()
    
    def InitUI(self):
        tb = self.CreateToolBar()
        qtool = tb.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('quit.png'))
        tb.Realize()
        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)
        
        l = DebuggerList(self)

        self.SetSize((300,200))
        self.SetTitle('Emulator')
        self.Centre()
        self.Show(True)
        
        
    def OnQuit(self, e):
        self.Close()
        
        
if __name__ == '__main__':
    ex = wx.App()
    Emulator(None)
    ex.MainLoop()