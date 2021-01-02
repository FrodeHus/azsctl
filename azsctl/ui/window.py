import asyncio
import urwid
from azsctl.ui import signals
from azsctl.ui.controller import Controller, RefreshableItems
from azsctl.ui.statusbar import StatusBar
from azsctl.ui.tabs import TabItem, TabPanel
from azsctl.ui.widgets import (
    SentinelItemList,
    SentinelItemListWalker,
    RuleItem,
    IncidentItem,
)


class Window(urwid.Frame):
    def __init__(self, controller: Controller):
        self.statusbar = StatusBar()
        self.controller = controller
        signals.focus.connect(self.signal_focus)

        def rule_retrieval_method():
            return [
                urwid.AttrMap(RuleItem(rule), None, focus_map="focus")
                for rule in self.controller.get_alert_rules()
            ]

        def incident_retrieval_method():
            return [
                urwid.AttrMap(IncidentItem(incident), None, focus_map="focus")
                for incident in self.controller.get_incidents()
            ]

        tabs = [
            TabItem(
                "Incident",
                urwid.AttrWrap(
                    SentinelItemList(
                        SentinelItemListWalker(
                            RefreshableItems(incident_retrieval_method, [])
                        )
                    ),
                    "background",
                ),
            ),
            TabItem(
                "Alert rule",
                urwid.AttrWrap(
                    SentinelItemList(
                        SentinelItemListWalker(
                            RefreshableItems(rule_retrieval_method, [])
                        )
                    ),
                    "background",
                ),
            ),
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
