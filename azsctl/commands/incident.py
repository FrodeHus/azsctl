from azsctl.commands.command import SubCommand
from azsctl import current_config
from azsctl.auth import TokenRequester
from azsctl.api import AzureSentinelApi
def list_incidents():
    token_requester = TokenRequester()
    api = AzureSentinelApi(token_requester)
    return api.get_incidents()