import wx
import plotter

VERSION = 1.0

class AppFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300,350))
        label1 = wx.StaticText(self, label="Start frekvens (10^)", pos=(20,20))
        label2 = wx.StaticText(self, label="Slut frekvens (10^) ", pos=(20,50))
        label3 = wx.StaticText(self, label="Målinger pr. dekade ", pos=(20,80))
        label4 = wx.StaticText(self, label="TF (Tæller) ", pos=(20,110))
        label5 = wx.StaticText(self, label="TF (Nævner) ", pos=(20, 140))


        label6 = wx.StaticText(self, label="Bode plotter version " + str(VERSION), pos=(20, 245))
        label7 = wx.StaticText(self, label="Dokumentation findes på\nhttps://math221e.github.io ", pos=(20, 265))

        self.input1 = wx.TextCtrl(self, value="1", pos=(150, 20), size=(140,-1))
        self.input2 = wx.TextCtrl(self, value="5", pos=(150, 50), size=(140,-1))
        self.input3 = wx.TextCtrl(self, value="20", pos=(150, 80), size=(140,-1))
        self.input4 = wx.TextCtrl(self, value="", pos=(150, 110), size=(140,-1))
        self.input5 = wx.TextCtrl(self, value="", pos=(150, 140), size=(140, -1))
        self.input6 = wx.CheckBox(self, id=wx.ID_ANY, label="Gem data til csv fil (bode_data.csv)", pos=(20, 170))

        self.plotButton = wx.Button(self, wx.ID_ANY, "Start", pos=(150, 200))

        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Klar")

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.plotButton)
        
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("./icon.png", wx.BITMAP_TYPE_PNG))
        self.SetIcon(icon)
        self.Show(True)

    def OnClick(self, event):
        plotter.bodeplot(self, self.input1.GetValue(), self.input2.GetValue(), self.input3.GetValue(), self.input4.GetValue(), self.input5.GetValue(), self.input6.GetValue())

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event

        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Bode plotter software specielt skrevet til Keysight/Agilent 2000 series. \n- Mathias Dam (matda19@student.sdu.dk).",
                      "Bode Plotter",
                      wx.OK|wx.ICON_INFORMATION)

class App(wx.App):
    def __init(self, parent):
        wx.App.__init__(self, parent)

app = App(False)
frame = AppFrame(None, "Bode plotter")
app.MainLoop()
