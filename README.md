# azsctl

![CodeQL](https://github.com/FrodeHus/azsctl/workflows/CodeQL/badge.svg)

Simple tool to do maintenace tasks with Azure Senitel from CLI instead of web - might change 'simple' to 'advanced' later.

## Installation

Tried to make it as simple as possible so... try:

`python3 -m pip install azsctl`

### Enable tab completion

`source azsentinel.completion.sh`

## Usage

`azsctl login` to get started.

```text
Group
    azsctl

Subgroups:
    alert            : Work with Azure Sentinel alerts.
    analytics        : Query data in your log analytics workspace.
    incident         : Work with Azure Sentinel incidents.
    rule             : Add/edit/view/delete/import Azure Sentinel alert rules.
    workspace        : View information about the workspace(s) you have access to.

Commands:
    login            : Log in to your Azure subscription and select which workspace to user with
                       Sentinel.
    select-workspace
    ui

```

## Acknowledgements

Took a lot of inspiration (and some code lines) from [mitmproxy](https://github.com/mitmproxy/mitmproxy) to bend [urwid](https://urwid.org) to my will.
