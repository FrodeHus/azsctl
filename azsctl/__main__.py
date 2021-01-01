import json
import os,sys
from textwrap import indent
from azsctl.api import AzureManagementApi, AzureSentinelApi
from azsctl.auth import TokenRequester
from PyInquirer import prompt
from azsctl import current_config
from knack import CLI
from knack.commands import CLICommandsLoader, CommandGroup
from knack.arguments import ArgumentsContext, CLIArgumentType
from knack.help import CLIHelp
from knack.help_files import helps


def login():
    token_requester = TokenRequester()
    management_api = AzureManagementApi(token_requester)
    subs = management_api.get_subscriptions()
    select_subscription = {
        "type": "list",
        "name": "subscription",
        "message": "Which subscription would you like to use?",
        "choices": [sub["displayName"] for sub in subs],
    }
    selection = prompt(select_subscription)
    subscription = (
        list(
            filter(
                lambda x: x["displayName"] == selection["subscription"], subs
            )
        )
    )[0]
    current_config.set_subscription(
        subscription["displayName"], subscription["subscriptionId"]
    )

def select_workspace():
    token_requester = TokenRequester()
    management_api = AzureManagementApi(token_requester)
    workspaces = management_api.get_workspaces()
    select_workspace = {
        "type": "list",
        "name": "workspace",
        "message": "Which workspace would you like to use?",
        "choices": [w["name"] for w in workspaces],
    }
    selection = prompt(select_workspace)
    workspace = list(
        filter(lambda x: x["name"] == selection["workspace"], workspaces)
    )[0]
    current_config.set_workspace(workspace["name"], workspace["id"])

helps[
    "config"
] = """
    type: group
    short-summary: Manage the CLI configuration.
"""


class CommandLoader(CLICommandsLoader):
    def load_command_table(self, args):
        with CommandGroup(self, "", "azsctl.__main__#{}") as g:
            g.command("login", "login")
            g.command("select-workspace", "select_workspace")
        with CommandGroup(self, "incident", "azsctl.commands.incident#{}") as g:
            g.command("list", "list_incidents")
        return super(CommandLoader, self).load_command_table(args)


class Help(CLIHelp):
    def __init__(self, cli_ctx=None):
        super(Help, self).__init__(
            cli_ctx=cli_ctx,
        )

name="azsctl"
cli = CLI(
    cli_name=name,
    config_dir=os.path.expanduser(os.path.join("~", ".{}".format(name))),
    config_env_var_prefix=name,
    commands_loader_cls=CommandLoader,
    help_cls=Help,
)
exit_code = cli.invoke(sys.argv[1:])
sys.exit(exit_code)
