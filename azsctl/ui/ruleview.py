import urwid
from .controller import Controller, RefreshableItems

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
        if key == 'enter':
            pass
        return urwid.ListBox.keypress(self, size, key)

class RuleListWalker(urwid.ListWalker):
    def __init__(self, retriever : RefreshableItems):
        self.retriever = retriever
        self.items = retriever.items
        self.focus = 0

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        return self._get_at_pos(start_from + 1)

    def get_prev(self, start_from):

        return self._get_at_pos(start_from - 1)

    def _get_at_pos(self, pos):
        if pos < 0:
            return None, None

        if len(self.items) > pos:
            return self.items[pos], pos

        return None, None
    
        
        
        
