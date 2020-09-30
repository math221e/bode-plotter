import wx
import plotter

class AppFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300,230))
        label1 = wx.StaticText(self, label="Start frekvens (10^)", pos=(20,20))
        label2 = wx.StaticText(self, label="Slut frekvens (10^) ", pos=(20,50))
        label3 = wx.StaticText(self, label="Målinger pr. dekade ", pos=(20,80))
        label4 = wx.StaticText(self, label="TF (NUM) ", pos=(20,110))
        label5 = wx.StaticText(self, label="TF (DEN) ", pos=(20, 140))

        self.input1 = wx.TextCtrl(self, value="1", pos=(150, 20), size=(140,-1))
        self.input2 = wx.TextCtrl(self, value="5", pos=(150, 50), size=(140,-1))
        self.input3 = wx.TextCtrl(self, value="20", pos=(150, 80), size=(140,-1))
        self.input4 = wx.TextCtrl(self, value="[1]", pos=(150, 110), size=(140,-1))
        self.input5 = wx.TextCtrl(self, value="[R*C, 1]", pos=(150, 140), size=(140, -1))

        self.plotButton = wx.Button(self, wx.ID_ANY, "GO", pos=(150, 170))

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.plotButton)
        self.Show(True)

    def OnClick(self, event):
        plotter.bodeplot(self.input1.GetValue(), self.input2.GetValue(), self.input3.GetValue(), self.input4.GetValue(), self.input5.GetValue())

class App(wx.App):
    def __init(self, parent):
        wx.App.__init__(self, parent)
        self.locale = wx.Locale(wx.en_US)

app = App(False)
frame = AppFrame(None, "Bode plotter")
app.MainLoop()
