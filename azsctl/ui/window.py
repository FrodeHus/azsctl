from azsctl.ui.statusbar import StatusBar
from .ruleview import RuleList, RuleListWalker, RuleItem
from .controller import Controller
import urwid
import asyncio

class Window(urwid.Frame):
    def __init__(self, controller : Controller):
        self.statusbar = StatusBar()
        self.controller = controller
        data = self.controller.get_alert_rules()
        items = [urwid.AttrMap(RuleItem(rule), None, focus_map="focus") for rule in data]
        super().__init__(
            urwid.ListBox(urwid.SimpleFocusListWalker(items)), header=None, footer=urwid.AttrWrap(self.statusbar, "background")
        )
