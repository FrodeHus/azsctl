from azsctl.ui.window import Window
from azsctl.ui import signals
import urwid


class AzsctlUI:
    def __init__(self) -> None:
        palette = [
            ("background", "", "", "", "h230", "h33"),
            ("body", "", "", "", "h254", "h235"),
        ]
        self.window = Window()
        self.loop = urwid.MainLoop(urwid.AttrWrap(self.window, "body"), palette=palette, unhandled_input=self.unhandled_input)
        self.loop.screen.set_terminal_properties(colors=256)
        def cb(*_):
            return callback(*args)
        self.loop.set_alarm_in(5, lambda sender,*args: signals.status_message.send(message="this is a test"))

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()