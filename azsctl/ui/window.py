from azsctl.ui.statusbar import StatusBar
from .ruleview import RuleList, RuleListWalker, RuleItem
from .controller import Controller, RefreshableItems
from azsctl.ui import signals
import urwid
import asyncio


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
            header=None,
            footer=urwid.AttrWrap(self.statusbar, "background"),
        )

    def signal_focus(self, sender, section):
        self.focus_position = section
