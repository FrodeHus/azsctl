import asyncio
import urwid
from azsctl.ui import signals
from azsctl.ui.controller import Controller, RefreshableItems
from azsctl.ui.statusbar import StatusBar
from azsctl.ui.widget import (
    IncidentView,
    TabItem,
    TabPanel,
)


class Window(urwid.Frame):
    def __init__(self, controller: Controller):
        self.statusbar = StatusBar([
            ('F1', 'Incidents'),
            ('F2', 'Alert rules'),
            ('F3', 'Hunting'),
            ('F4', 'Threat indicators'),
            ('F5', 'Analytics'),
        ])
        self.controller = controller
        signals.focus.connect(self.signal_focus)
        self.windows = [
            IncidentView(),
            urwid.Pile([])
        ]
        super().__init__(
            self.windows[0],
            footer=urwid.AttrWrap(self.statusbar, "background"),
        )

    def keypress(self, size, key):
        if key == "f1":
            self.body = self.windows[0]
        if key == "f2":
            self.body = self.windows[1]
        
        return super().keypress(size, key)

    def signal_focus(self, sender, section):
        self.focus_position = section
