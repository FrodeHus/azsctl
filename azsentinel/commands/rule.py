import json
import yaml
from azsentinel.api import AzureSentinelApi
from azsentinel.classes import ScheduledAlertRule, ScheduledAlertRuleTemplate
from azsentinel.commands.analytics import execute_query
from azsentinel.validators import ScheduledRuleValidator
from PyInquirer.prompt import prompt
import os


def backup_rules(folder: str = None):
    """
    Retrieves all alert rules and saves them as individual files
    """
    rules = list_rules()
    for rule in rules:
        name = rule["properties"]["displayName"]
        del rule["properties"]["lastModifiedUtc"]
        filename = "".join(x for x in name.title() if not x.isspace())
        if not folder:
            folder = os.getcwd()
        elif not os.path.exists(folder):
            os.makedirs(folder)

        filename = os.path.join(folder, f"{filename}.json")
        with open(filename, "w") as rule_file:
            json.dump(rule, rule_file, indent=2)


def restore_rules(rule_file: str = None, folder: str = None):
    """
    Restore single rule from file or all rules found in specified folder.
    This will overwrite existing rules even if newer.
    """
    rules = []
    if folder:
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            rules.append(full_path)
    elif rule_file:
        rules.append(rule_file)

    api = AzureSentinelApi()
    for file in rules:
        with open(file, "r") as rule_file:
            rule = json.load(rule_file)
        rule_id = rule["name"]
        existing = get_rule(rule_id)
        name = rule["properties"]["displayName"]
        if existing:
            etag = existing["etag"]
            rule["etag"] = etag
            result = api.update_alert_rule(rule_id, rule)
            if "status_code" in result:
                code = result["content"]["error"]["code"]
                message = result["content"]["error"]["message"]
                print(f"Failed to restore rule {name} - {code} : {message}")
                continue
            print("Restored " + rule["properties"]["displayName"])


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
