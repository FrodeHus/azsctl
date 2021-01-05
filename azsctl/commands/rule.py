import json
import yaml
from azsctl.api import AzureSentinelApi
from azsctl.classes import ScheduledAlertRule, ScheduledAlertRuleTemplate
from azsctl.commands.analytics import execute_query
from azsctl.validators import ScheduledRuleValidator
from PyInquirer.prompt import prompt


def list_rules():
    """
    Lists all alert rules in the active workspace
    """
    api = AzureSentinelApi()
    return api.get_alert_rules()


def get_rule(rule_id: str):
    """
    Retrieve and display alert rule
    """
    api = AzureSentinelApi()
    return api.get_alert_rule(rule_id)


def run_rule_query(rule_id: str = None):
    """
    Executes the query in the specified alert rule and returns the results
    """
    if not rule_id:
        rule_id = select_rule()

    rule = get_rule(rule_id)
    query = rule["properties"]["query"]
    data = execute_query(query)
    return data


def edit_rule(rule_id: str = None):
    """
    Edit alert rule
    """
    if not rule_id:
        rule_id = select_rule()

    import json
    import os
    import tempfile
    from subprocess import call

    api = AzureSentinelApi()
    EDITOR = os.getenv("EDITOR", "vim")
    rule = get_rule(rule_id)
    del rule["properties"]["lastModifiedUtc"]

    with tempfile.NamedTemporaryFile(suffix=".rule", delete=False, mode="w") as temp:
        rule_to_edit = json.dumps(rule, indent=2)
        temp.write(rule_to_edit)
        temp.flush()
        call([EDITOR, temp.name], shell=False)

    with open(temp.name, "r") as edited_rule:
        rule = json.load(edited_rule)
        result = api.update_alert_rule(rule_id, rule)

    os.remove(temp.name)
    return result


def import_rule(file: str, validate_only: bool = False):
    """
    Import alert rule from YAML
    """
    with open(file, "r") as f:
        document = yaml.full_load(f)

    rule_template = ScheduledAlertRuleTemplate.from_yaml_template(document)
    result, message = validate_rule(rule_template)
    if not result:
        return message
    return rule_template


def validate_rule(rule: ScheduledAlertRuleTemplate):
    validator = ScheduledRuleValidator(rule)
    return validator.validate()


def select_rule():
    rules = list_rules()
    select = {
        "type": "list",
        "name": "rule",
        "message": "Which alert rule do you wish to use?",
        "choices": [rule["properties"]["displayName"] for rule in rules],
    }

    answer = prompt(select)
    rule_id = (
        list(filter(lambda x: x["properties"]["displayName"] == answer["rule"], rules))
    )[0]
    return rule_id["name"]

def list_alert_rule_templates():
    api = AzureSentinelApi()
    return api.list_alert_rule_templates()
