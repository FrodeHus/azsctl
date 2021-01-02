from azsctl.ui.window import Window
import urwid


class AzsctlUI:
    def __init__(self) -> None:
        palette = [
            ("background", "", "", "", "", "h245"),
            ("body", "", "", "", "h254", "h235")
        ]
        self.window = Window()
        self.loop = urwid.MainLoop(urwid.AttrWrap(self.window, "body"), palette=palette, unhandled_input=self.unhandled_input)
        self.loop.screen.set_terminal_properties(colors=256)

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()