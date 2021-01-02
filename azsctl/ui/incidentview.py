import urwid
from .controller import Controller, RefreshableItems

class IncidentItem(urwid.WidgetWrap):
    def __init__(self, incident):
        self.incident = incident
        w = self.get_rule_text()
        super().__init__(w)

    def selectable(self):
        return True

    def get_rule_text(self):
        return urwid.Columns([
            urwid.Text(self.incident["properties"]["title"]),
            urwid.Text(self.incident["properties"]["severity"]),
            urwid.Text(self.incident["properties"]["status"]),
        ], dividechars=1)
