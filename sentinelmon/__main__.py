import argparse
import json
from textwrap import indent
from sentinelmon.api import AzureManagementApi, AzureSentinelApi
from sentinelmon.auth import TokenRequester
from PyInquirer import prompt
from sentinelmon import current_config

parser = argparse.ArgumentParser(
    prog="sentinelmon", description="Simple Azure Sentinel monitor"
)

subparsers = parser.add_subparsers(dest="group")
incident_parser = subparsers.add_parser("incident", help="Incident subcommands")
incident_parser.add_argument(
    "--list-incidents", action="store_true", help="Lists all active incidents"
)

rule_parser = subparsers.add_parser("rule", help="Rule subcommands")

group = parser.add_argument_group()

group.add_argument(
    "--login", action="store_true", help="Log in to your Azure subscription"
)
group.add_argument(
    "--select-workspace",
    action="store_true",
    help="Retrieves all workspaces and lets you select which to set as active",
)
group.add_argument(
    "--show-workspace",
    action="store_true",
    help="Displays metadata about the currently selected workspace",
)
args = parser.parse_args()
token_requester = TokenRequester()
management_api = AzureManagementApi(token_requester)


def login():
    global management_api
    subs = management_api.get_subscriptions()
    select_subscription = {
        "type": "list",
        "name": "subscription",
        "message": "Which subscription would you like to use?",
        "choices": [sub["displayName"] for sub in subs["value"]],
    }
    selection = prompt(select_subscription)
    subscription = (
        list(
            filter(
                lambda x: x["displayName"] == selection["subscription"], subs["value"]
            )
        )
    )[0]
    current_config.set_subscription(
        subscription["displayName"], subscription["subscriptionId"]
    )
    select_workspace()


def select_workspace():
    global config, management_api
    workspaces = management_api.get_workspaces()
    select_workspace = {
        "type": "list",
        "name": "workspace",
        "message": "Which workspace would you like to use?",
        "choices": [w["name"] for w in workspaces["value"]],
    }
    selection = prompt(select_workspace)
    workspace = list(
        filter(lambda x: x["name"] == selection["workspace"], workspaces["value"])
    )[0]
    current_config.set_workspace(workspace["name"], workspace["id"])


def show_workspace():
    global config, management_api
    workspace = management_api.get_current_workspace()
    print(json.dumps(workspace, indent=2))


def list_incidents():
    global token_requester
    api = AzureSentinelApi(token_requester)
    incidents = api.get_incidents()
    print(json.dumps(incidents, indent=2))


def main():
    global args
    if args.login:
        login()
    if args.select_workspace:
        select_workspace()
    if args.show_workspace:
        show_workspace()
    if args.group == "incident":
        if args.list_incidents:
            list_incidents()


if __name__ == "__main__":
    main()