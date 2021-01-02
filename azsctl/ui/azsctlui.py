from azsctl.ui.window import Window
import urwid

class AzsctlUI:
    def __init__(self) -> None:
        self.loop = urwid.MainLoop(Window())
    
    def run(self):
        self.loop.run()