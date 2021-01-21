import asyncio
from azsentinel.ui.widget.dialog import Dialog
import urwid
from azsentinel.ui import signals
from azsentinel.ui.controller import Controller
from azsentinel.ui.statusbar import StatusBar
from azsentinel.ui.widget import (
    IncidentView,
    TabItem,
    TabPanel,
)


class Window(urwid.Frame):
    SIGNAL_VIEW_INCIDENTS = "view_incidents"
    SIGNAL_VIEW_RULES = "view_rules"
    SIGNAL_VIEW_HUNTING = "view_hunting"
    SIGNAL_VIEW_THREATS = "view_threats"
    SIGNAL_VIEW_ANALYTICS = "view_analytics"
    SIGNALS = [SIGNAL_VIEW_INCIDENTS, SIGNAL_VIEW_RULES, SIGNAL_VIEW_HUNTING, SIGNAL_VIEW_THREATS, SIGNAL_VIEW_ANALYTICS]
    def __init__(self, controller: Controller):
        urwid.register_signal(self.__class__, self.SIGNALS)
        self.statusbar = StatusBar([
            ('F1', 'Incidents', self.SIGNAL_VIEW_INCIDENTS),
            ('F2', 'Alert rules', self.SIGNAL_VIEW_RULES),
            ('F3', 'Hunting', self.SIGNAL_VIEW_HUNTING),
            ('F4', 'Threat indicators', self.SIGNAL_VIEW_THREATS),
            ('F5', 'Analytics', self.SIGNAL_VIEW_ANALYTICS),
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
