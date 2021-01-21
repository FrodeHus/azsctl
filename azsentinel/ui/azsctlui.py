from azsentinel.ui.window import Window
from azsentinel.ui import signals
from .controller import Controller
import urwid
class AzsctlUI:
    def __init__(self, controller : Controller) -> None:
        palette = [
            ("background", "", "black"),
            ("body", "","black"),
            ("heading", "white", "dark blue"),
            ("heading inactive", "light gray", "light blue"),
            ("focus", "","", "", "#fdf6e3", "#93a1a1"),
            ("actionbar:action", "white", "black"),
            ("important", 'dark blue','black',('standout','underline'))
        ]
        async_loop = controller.async_loop
        event_loop = urwid.AsyncioEventLoop(loop=async_loop)
        self.controller = controller
        self.window = Window(controller)
        self.loop = urwid.MainLoop(urwid.AttrWrap(self.window, "body"), palette=palette, unhandled_input=self.unhandled_input, event_loop=event_loop)
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