import sys
from azsctl.commands.command import SubCommand
from azsctl import current_config
from azsctl.api import AzureSentinelApi
def list_incidents():
    _, id = current_config.get_workspace()
    if not id:
        print("No workspace selected - try azsctl select-workspace")
        sys.exit(1)
    api = AzureSentinelApi()
    return api.get_incidents()