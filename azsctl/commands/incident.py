import sys
from azsctl import current_config
from azsctl.api import AzureSentinelApi


def list_incidents():
    _, workspace_id = current_config.get_workspace()
    if not workspace_id:
        print("No workspace selected - try azsctl select-workspace")
        sys.exit(1)
    api = AzureSentinelApi()
    return api.get_incidents()


def get_incident(id: str):
    api = AzureSentinelApi()
    return api.get_incident(id)
