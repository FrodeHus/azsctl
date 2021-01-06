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

    def keypress(self, size, key):
        if key in ("esc"):
            self.hide_incident()
        return super().keypress(size, key)

    def hide_incident(self):
        if self.incident_detail:
            self.incident_detail = None
        self._w = self.main_list

    def load_incidents(self):
        incidents = self.api.get_incidents("properties/status ne 'Closed'")
        return [
            urwid.AttrMap(IncidentItem(incident), None, focus_map="focus")
            for incident in incidents
        ]

    def show_incident(self, incident):
        if not incident:
            return
        self.incident_detail = IncidentDetailView(incident)
        self._w = urwid.Pile(
            [self.main_list, self.incident_detail], focus_item=self.incident_detail
        )

    def handle_item_selected(self, sender, item):
        self.show_incident(item)


class IncidentDetailView(urwid.WidgetWrap):
    def __init__(self, incident):
        self.incident = incident
        self._body = urwid.LineBox(
            urwid.Filler(urwid.Text(json.dumps(incident, indent=2)), "middle")
        )
        self._frame = urwid.Frame(self._body)
        super().__init__(self._frame)

    def selectable(self):
        return True


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
        owner = self.data["properties"]["owner"]["userPrincipalName"]
        if not owner:
            owner = "Unassigned"
        return urwid.Columns(
            [
                ('weight', 4 , urwid.Text(self.data["properties"]["title"])),
                ('weight', 1, urwid.Text(self.data["properties"]["severity"])),
                ('weight', 1, urwid.Text(self.data["properties"]["status"])),
                ('weight', 2, urwid.Text(owner)),
            ],
            dividechars=1,
        )
