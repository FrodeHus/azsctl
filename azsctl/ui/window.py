import asyncio
import urwid
from azsctl.ui import signals
from azsctl.ui.controller import Controller, RefreshableItems
from azsctl.ui.statusbar import StatusBar
from azsctl.ui.widget import (
    IncidentView,
    SentinelItemList,
    SentinelItemListWalker,
    RefreshableItems,
    RuleItem,
    IncidentItem,
    TabItem,
    TabPanel,
)


class Window(urwid.Frame):
    def __init__(self, controller: Controller):
        self.statusbar = StatusBar()
        self.controller = controller
        signals.focus.connect(self.signal_focus)

        incident_view = IncidentView()
        tabs = [
            TabItem(
                "Incident",
                urwid.AttrWrap(
                    incident_view,
                    "background",
                ),
            ),
            TabItem("Alert rule", urwid.Pile([])),
            TabItem("Hunting", urwid.Pile([])),
            TabItem("Threat indicators", urwid.Pile([])),
            TabItem("Analytics", urwid.Pile([])),
        ]

        super().__init__(
            TabPanel(tabs),
            footer=urwid.AttrWrap(self.statusbar, "background"),
        )

    def signal_focus(self, sender, section):
        self.focus_position = section
