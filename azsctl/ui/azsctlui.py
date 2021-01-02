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
            ("focus", "light magenta", "black")
        ]
        self.controller = controller
        self.window = Window(controller)
        self.loop = urwid.MainLoop(urwid.AttrWrap(self.window, "body"), palette=palette, unhandled_input=self.unhandled_input)
        self.loop.screen.set_terminal_properties(colors=256)
        signals.delayed_signal.connect(self.signal_delayed)
        signals.status_message.send(message="Timed message - should go away after 5 seconds", expire=5)

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()

    def signal_delayed(self, sender, seconds, callback, args=()):
        def cb(*_):
            return callback(*args)
        self.loop.set_alarm_in(seconds, cb)