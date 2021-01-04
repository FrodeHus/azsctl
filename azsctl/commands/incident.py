import sys
from azsctl import current_config
from azsctl.api import AzureSentinelApi


def list_incidents():
    """
    Retrieves all non-closed incidents
    """
    _, workspace_id = current_config.get_workspace()
    if not workspace_id:
        print("No workspace selected - try azsctl select-workspace")
        sys.exit(1)
    api = AzureSentinelApi()
    return api.get_incidents()


def get_incident(id: str):
    """
    Retrieves specified incident
    """
    api = AzureSentinelApi()
    return api.get_incident(id)

def get_incident_alerts(id : str):
    """
    Retrieves the alerts connected to the specified incident
    """
    api = AzureSentinelApi()
    return api.get_incident_alerts(id)

def get_incident_events(id : str):
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

