import json
import os,sys
from textwrap import indent
from azsctl.api import AzureManagementApi, AzureSentinelApi
from PyInquirer import prompt
from azsctl import current_config
from knack import CLI, experimental
from knack.commands import CLICommandsLoader, CommandGroup
from knack.arguments import ArgumentsContext, CLIArgumentType
from knack.help import CLIHelp
from knack.help_files import helps
from azsctl.ui import AzsctlUI
from azsctl.ui.controller import Controller


def login():
    management_api = AzureManagementApi()
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
    management_api = AzureManagementApi()
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

def show_ui():
    """
    Opens interactive UI
    """
    ui = AzsctlUI(Controller())
    ui.run()

helps[
    "login"
] = """
type: command
short-summary: Log in to your Azure subscription and select which workspace to user with Sentinel.
"""

helps["incident"] = """
type: group
short-summary: Work with Azure Sentinel incidents
"""

helps["alert"] = """
type: group
short-summary: Work with Azure Sentinel alerts
"""

helps["rule"] = """
type: group
short-summary: Add/edit/view/delete/import Azure Sentinel alert rules
"""

helps["analytics"] = """
type: group
short-summary: Query data in your log analytics workspace
"""

helps["workspace"] = """
type: group
short-summary: View information about the workspace(s) you have access to
"""

class CommandLoader(CLICommandsLoader):
    def load_command_table(self, args):
        with CommandGroup(self, "", "azsctl.__main__#{}") as g:
            g.command("login", "login")
            g.command("select-workspace", "select_workspace")
            g.command("ui", "show_ui", is_experimental=True)
        with CommandGroup(self, "incident", "azsctl.commands.incident#{}") as g:
            g.command("list", "list_incidents")
            g.command("alerts", "get_incident_alerts")
            g.command("alert-events", "get_incident_events")
            g.command("show", "get_incident")
        with CommandGroup(self, "rule", "azsctl.commands.rule#{}") as g:
            g.command("list", "list_rules")
            g.command("show", "get_rule")
            g.command("edit", "edit_rule")
            g.command("run", "run_rule_query")
            g.command("import", "import_rule", confirmation=True)
        with CommandGroup(self, "alert", "azsctl.commands.alert#{}") as g:
            g.command("show", "get_alert")
            g.command("events", "get_alert_events")
        with CommandGroup(self, "analytics", "azsctl.commands.analytics#{}") as g:
            g.command("query", "execute_query")
        with CommandGroup(self, "analytics datasource", "azsctl.commands.analytics#{}") as g:
            g.command("list", "list_datasources")
        with CommandGroup(self, "workspace", "azsctl.commands.workspace#{}") as g:
            g.command("show", "show_workspace")
            g.command("list", "list_workspaces")
        return super(CommandLoader, self).load_command_table(args)
    
    def load_arguments(self, command):
        with ArgumentsContext(self, 'rule import') as ac:
            ac.argument('validate-only', type=bool)
        super(CommandLoader, self).load_arguments(command)


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

if len(sys.argv) == 1:
    show_ui()
else:    
    exit_code = cli.invoke(sys.argv[1:])
    sys.exit(exit_code)
