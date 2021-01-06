from azsctl.ui.widget.tabs import TabPanel, TabItem
from azsctl.ui.widget.list import SentinelItemList
from azsctl.api import AzureSentinelApi
import urwid

class IncidentView(urwid.WidgetWrap):
    def __init__(self):
        self.api = AzureSentinelApi()
        self.main_list = SentinelItemList(self.load_incidents)
        self.show_detail = False
        urwid.connect_signal(self.main_list, "item_selected", self.handle_item_selected)
        urwid.WidgetWrap.__init__(self, self.main_list)        

    def keypress(self, size, key):
        if key in ("esc"):
            self.hide_incident()
        if key == "tab" and self.show_detail:
            self.switch_focus()
        return super().keypress(size, key)

    def switch_focus(self):
        self.detail_view.focus_position = (
            0 if self.detail_view.focus_position == 1 else 1
        )

    def hide_incident(self):
        self.show_detail = False
        if self.detail_view:
            del self.detail_view
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
        self.show_detail = True
        incident_detail = IncidentDetailView(incident)
        tabs = TabPanel(
            [
                TabItem("Overview", incident_detail),
                TabItem("Entities", urwid.Pile([])),
                TabItem("Events", IncidentEventView(incident)),
            ]
        )
        self.detail_view = urwid.Pile([self.main_list, tabs], 1)

        self._w = self.detail_view

    def handle_item_selected(self, sender, item):
        self.show_incident(item)


class IncidentEventView(urwid.WidgetWrap):
    def __init__(self, incident):
        self.api = AzureSentinelApi()
        self.incident = incident
        self._body = urwid.Filler(urwid.Text(["Press '",("important", "r"), "' to load events (could take a while)"], align="center"), 'middle')
        self.is_first_view = True
        super().__init__(self._body)

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == "r" and self.is_first_view:
            self._w = urwid.Filler(urwid.Text("Please wait...", align="center"), "middle")
            self._body = self.prepare_view()
            self._w = self._body
            self.is_first_view = False
        
        return key

    def load_events(self):
        alerts = self.api.get_incident_alerts(self.incident["name"])
        events = []
        for alert in alerts:
            alert_events = self.api.get_alert_events(alert["name"])
            events = events + alert_events
        return [
            urwid.AttrMap(AlertEventItem(ev), None, focus_map="focus")
            for ev in events
        ]

    def prepare_view(self):
        event_list = SentinelItemList(self.load_events)
        return event_list

class IncidentDetailView(urwid.WidgetWrap):
    def __init__(self, incident):
        self.incident = incident
        self._body = self.header()
        self._frame = urwid.Frame(self._body)
        super().__init__(self._frame)

    def header(self):
        title = self.incident["properties"]["title"]
        description = self.incident["properties"]["description"]
        severity = self.incident["properties"]["severity"]
        status = self.incident["properties"]["status"]
        owner = self.incident["properties"]["owner"]["userPrincipalName"]
        if not owner:
            owner = "Unassigned"
        header = urwid.Filler(
            urwid.LineBox(
                urwid.Pile(
                    [
                        urwid.Columns(
                            [
                                ("weight", 1, urwid.Text(("important", "Title"))),
                                ("weight", 4, urwid.Text(title)),
                            ]
                        ),
                        urwid.Columns(
                            [
                                (
                                    "weight",
                                    1,
                                    urwid.Text(("important", "Description")),
                                ),
                                ("weight", 4, urwid.Text(description)),
                            ],
                        ),
                        urwid.Columns(
                            [
                                ("weight", 1, urwid.Text(("important", "Severity"))),
                                ("weight", 4, urwid.Text(severity)),
                            ]
                        ),
                        urwid.Columns(
                            [
                                ("weight", 1, urwid.Text(("important", "Status"))),
                                ("weight", 4, urwid.Text(status)),
                            ]
                        ),
                        urwid.Columns(
                            [
                                ("weight", 1, urwid.Text(("important", "Assigned"))),
                                ("weight", 4, urwid.Text(owner)),
                            ]
                        ),
                    ]
                )
            ),
            "top",
        )
        return header

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
                ("weight", 4, urwid.Text(self.data["properties"]["title"])),
                ("weight", 1, urwid.Text(self.data["properties"]["severity"])),
                ("weight", 1, urwid.Text(self.data["properties"]["status"])),
                ("weight", 2, urwid.Text(owner)),
            ],
            dividechars=1,
        )


class AlertEventItem(urwid.WidgetWrap):
    def __init__(self, event_row):
        self.data = event_row
        w = self.get_event_label()
        super().__init__(w)

    def get_event_label(self):
        fields = []
        for col in self.data.keys():
            value = self.data[col]
            fields.append(urwid.Text(str(value)))
        return urwid.Columns(fields, dividechars=1)