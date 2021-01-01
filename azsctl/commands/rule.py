from azsctl import current_config
from azsctl.api import AzureSentinelApi
from azsctl.validators import ScheduledRuleValidator
import yaml
from azsctl.commands.analytics import execute_query

def list_rules():
    api = AzureSentinelApi()
    return api.get_alert_rules()

def get_rule(rule_id : str):
    api = AzureSentinelApi()
    return api.get_alert_rule(rule_id)

def run_rule_query(rule_id : str):
    rule = get_rule(rule_id)
    query = rule["properties"]["query"]
    data = execute_query(query)
    return data

def import_rule(file : str, validate_only : bool = False):
    with open(file,"r") as f:
        documents = yaml.full_load(f)

    validation_results = {}
    for item, doc in documents.items():
        validation_results[f"rule_{item}"] = validate_rule(doc)
    if validate_only:
        return validation_results

def validate_rule(rule : dict):
    validator = ScheduledRuleValidator(rule)
    return validator.validate()