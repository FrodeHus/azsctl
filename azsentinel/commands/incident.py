import sys
from azsentinel import current_config
from azsentinel.api import AzureSentinelApi
from azsentinel.auth import TokenRequester


def list_incidents(
    only_assigned: bool = False, filter: str = "properties/status ne 'Closed'"
):
    """
    Retrieves a list of incidents (default: non-closed)
    """
    _, workspace_id = current_config.get_workspace()
    if not workspace_id:
        print("No workspace selected - try azsctl select-workspace")
        sys.exit(1)
    api = AzureSentinelApi()
    if only_assigned:
        _, user_id = TokenRequester().get_current_user()
        filter = f"{filter} and properties/owner/objectId eq '{user_id}'"

    return api.get_incidents(filter)


def get_incident(id: str):
    """
    Retrieves specified incident
    """
    api = AzureSentinelApi()
    return api.get_incident(id)


def get_incident_alerts(id: str):
    """
    Retrieves the alerts connected to the specified incident
    """
    api = AzureSentinelApi()
    return api.get_incident_alerts(id)


def get_incident_events(id: str):
    """
    Retrieves the events of all alerts connected to specified incident
    """
    api = AzureSentinelApi()
    alerts = api.get_incident_alerts(id)
    events = []
    for alert in alerts:
        alert_events = api.get_alert_events(alert["name"])
        events = events + alert_events

    return events


def get_incident_entities(id: str):
    """
    Retrieves the entities involved in specified incident
    """
    api = AzureSentinelApi()
    entities = api.get_incident_entities(id)
    items = []
    for entity in entities:
        item = {}
        item["kind"] = entity["kind"]
        item.update(entity["properties"])
        items.append(item)
    return items
