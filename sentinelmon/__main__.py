import argparse
import json
from textwrap import indent
from sentinelmon.config import Config
from sentinelmon.api import AzureManagementApi, AzureSentinelApi
from sentinelmon.auth import TokenRequester
from PyInquirer import prompt

parser = argparse.ArgumentParser(
    prog="sentinelmon", description="Simple Azure Sentinel monitor"
)

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

config = Config()


def login():
    global config, management_api
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
    config.set(Config.SUBSCRIPTION, subscription["displayName"])
    config.set(Config.SUBSCRIPTION_ID, subscription["subscriptionId"])
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
    config.set(Config.WORKSPACE, workspace["name"])
    config.set(Config.WORKSPACE_ID, workspace["id"])


def show_workspace():
    global config, management_api
    workspace = management_api.get_current_workspace()
    print(json.dumps(workspace, indent=2))


def main():
    global args
    if args.login:
        login()
    if args.select_workspace:
        select_workspace()
    if args.show_workspace:
        show_workspace()

if __name__ == "__main__":
    main()