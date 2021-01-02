from azsctl.ui.statusbar import StatusBar
import urwid

class Window(urwid.Frame):
    def __init__(self):
        self.statusbar = StatusBar()
        text = urwid.Text("testing")
        fill = urwid.Filler(text, "top")
        super().__init__(fill, header=None, footer=urwid.AttrWrap(self.statusbar, "background"))


        

        