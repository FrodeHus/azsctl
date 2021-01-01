from azsctl import current_config
from azsctl.api import AzureSentinelApi
import yaml

def list_rules():
    api = AzureSentinelApi()
    return api.get_alert_rules()

def get_rule(rule_id : str):
    api = AzureSentinelApi()
    return api.get_alert_rule(rule_id)

def import_rule(file : str, validate_only : bool = False):
    with open(file,"r") as f:
        documents = yaml.full_load(f)
    if validate_only:
        return True

    for item, doc in documents.items():
        print(item, ":", doc)