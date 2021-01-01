import sys
from azsctl.commands.command import SubCommand
from azsctl import current_config
from azsctl.auth import TokenRequester
from azsctl.api import AzureSentinelApi
def list_incidents():
    _, id = current_config.get_workspace()
    if not id:
        print("No workspace selected - try azsctl select-workspace")
        sys.exit(1)
    token_requester = TokenRequester()
    api = AzureSentinelApi(token_requester)
    return api.get_incidents()