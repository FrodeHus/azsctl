import json
from azsctl.ui.widget.list import SentinelItemList
from azsctl.api import AzureSentinelApi
import urwid

class IncidentView(urwid.WidgetWrap):
    def __init__(self):
        self.api = AzureSentinelApi()
        self.main_list = SentinelItemList(self.load_incidents)
        urwid.connect_signal(self.main_list, "item_selected", self.handle_item_selected)
        urwid.WidgetWrap.__init__(self, self.main_list)

    def load_incidents(self):
        incidents = self.api.get_incidents("properties/status ne 'Closed'")
        return [
                urwid.AttrMap(IncidentItem(incident), None, focus_map="focus")
                for incident in incidents
            ]

    def show_incident(self, incident):
        if not incident:
            return
        
        self._w = urwid.Pile([self.main_list, urwid.LineBox(urwid.Filler(urwid.Text(json.dumps(incident, indent=2)), 'middle'))])
        

    def handle_item_selected(self, sender, item):
        self.show_incident(item)
        

class IncidentItem(urwid.WidgetWrap):
    def __init__(self, incident):
        self.data = incident
        w = self.get_rule_text()
        super().__init__(w)

    def get_data(self):
        return self.data

    def selectable(self):
        return True

    def get_rule_text(self):
        return urwid.Columns([
            urwid.Text(self.data["properties"]["title"]),
            urwid.Text(self.data["properties"]["severity"]),
            urwid.Text(self.data["properties"]["status"]),
        ], dividechars=1)
