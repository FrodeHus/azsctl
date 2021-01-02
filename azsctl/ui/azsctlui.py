from azsctl.ui.window import Window
from azsctl.ui import signals
from .controller import Controller
import urwid


class AzsctlUI:
    def __init__(self, controller : Controller) -> None:
        palette = [
            ("background", "", "black"),
            ("body", "","black"),
            ("heading", "white", "dark blue"),
            ("focus", "light magenta", "light gray")
        ]
        self.controller = controller
        self.window = Window(controller)
        self.loop = urwid.MainLoop(urwid.AttrWrap(self.window, "body"), palette=palette, unhandled_input=self.unhandled_input)
        self.loop.screen.set_terminal_properties(colors=256)
        signals.delayed_signal.connect(self.signal_delayed)

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if key == ':':
            signals.action_command.send(cmd=':')
        elif key == 'esc':
            signals.action_singlecommand.send(cmd='back')
        

    def run(self):
        self.loop.run()

    def signal_delayed(self, sender, seconds, callback, args=()):
        def cb(*_):
            return callback(*args)
        self.loop.set_alarm_in(seconds, cb)