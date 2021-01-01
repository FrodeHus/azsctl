from PyInquirer.prompt import prompt
from azsctl.api import AzureSentinelApi
from azsctl.validators import ScheduledRuleValidator
import yaml
from azsctl.commands.analytics import execute_query


def list_rules():
    api = AzureSentinelApi()
    return api.get_alert_rules()


def get_rule(rule_id: str):
    api = AzureSentinelApi()
    return api.get_alert_rule(rule_id)


def run_rule_query(rule_id: str):
    rule = get_rule(rule_id)
    query = rule["properties"]["query"]
    data = execute_query(query)
    return data


def edit_rule(rule_id: str = None):
    if not rule_id:
        rule_id = select_rule()

    from subprocess import call
    import tempfile, os, json

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
    with open(file, "r") as f:
        documents = yaml.full_load(f)

    validation_results = {}
    for item, doc in documents.items():
        validation_results[f"rule_{item}"] = validate_rule(doc)
    if validate_only:
        return validation_results


def validate_rule(rule: dict):
    validator = ScheduledRuleValidator(rule)
    return validator.validate()


def select_rule():
    rules = list_rules()
    select = {
        "type": "list",
        "name": "rule",
        "message": "Which rule do you wish to edit?",
        "choices": [rule["properties"]["displayName"] for rule in rules],
    }

    answer = prompt(select)
    rule_id = (
        list(filter(lambda x: x["properties"]["displayName"] == answer["rule"], rules))
    )[0]
    return rule_id["name"]
