from azsctl.ui.statusbar import StatusBar
from .ruleview import RuleList, RuleListWalker, RuleItem
from .controller import Controller, RefreshableItems
from azsctl.ui import signals
import urwid
import asyncio


class TopMenu(urwid.WidgetWrap):
    def __init__(self):
        w = urwid.Columns(
            [
                urwid.Button("Incident"),
                urwid.Button("Alert Rule"),
                urwid.Button("Hunting"),
                urwid.Button("Analytics"),
            ], dividechars=2
        )
        urwid.WidgetWrap.__init__(self, urwid.AttrMap(w, "heading"))


class Window(urwid.Frame):
    def __init__(self, controller: Controller):
        self.statusbar = StatusBar()
        self.controller = controller
        signals.focus.connect(self.signal_focus)

        def retrieval_method():
            return [
                urwid.AttrMap(RuleItem(rule), None, focus_map="focus")
                for rule in self.controller.get_alert_rules()
            ]

        super().__init__(
            RuleList(RuleListWalker(RefreshableItems(retrieval_method, []))),
            header=TopMenu(),
            footer=urwid.AttrWrap(self.statusbar, "background"),
        )

    def signal_focus(self, sender, section):
        self.focus_position = section
