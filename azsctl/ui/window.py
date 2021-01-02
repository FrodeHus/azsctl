from azsctl.ui.statusbar import StatusBar
import urwid

class Window(urwid.Frame):
    def __init__(self):
        self.statusbar = StatusBar()
        super().__init__(header=None, footer=self.statusbar)

        