import urwid
from .controller import Controller

class RuleItem(urwid.WidgetWrap):
    def __init__(self, alert_rule):
        self.alert_rule = alert_rule
        w = self.get_rule_text()
        super().__init__(w)

    def selectable(self):
        return True

    def get_rule_text(self):
        return urwid.Columns([
            urwid.Text(self.alert_rule["properties"]["displayName"]),
            urwid.Text(self.alert_rule["name"], align="right")
        ], dividechars=2)

class RuleList(urwid.ListBox):

    def keypress(self, size, key):
        return key

class RuleListWalker(urwid.ListWalker):
    def __init__(self, controller : Controller):
        self.controller = controller
        
        
