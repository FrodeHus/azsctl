from azsentinel.classes import AlertRuleKind
from azsentinel import current_config
import requests
import sys
import json
from .auth import TokenRequester

base_url = "https://management.azure.com"


class BaseApi:
    def __init__(self):
        self._token_requester = TokenRequester()

    def get_access_token(self):
        token = self._token_requester.acquire_token()
        return token

    def get(self, path: str):
        try:
            result = requests.get(
                f"{base_url}/{path}",
                headers={"Authorization": self._get_authorization_header()},
            ).json()
            return result
        except Exception as error:
            print(error)
            sys.exit(1)

    def post(self, path: str, payload: any, url: str = base_url):
        try:
            result = requests.post(
                f"{url}/{path}",
                data=json.dumps(payload),
                headers={"Authorization": self._get_authorization_header()},
            )
            return result.json()
        except Exception as error:
            print(error)
            sys.exit(1)

    def put(self, path: str, payload: any, url: str = base_url):
        try:
            result = requests.put(
                f"{url}/{path}",
                json=payload,
                headers={"Authorization": self._get_authorization_header()},
            )

            if result.status_code != 200:
                error = {
                    "status_code": result.status_code,
                    "content": result.json()
                }
                return error

            return result.json()
        except Exception as error:
            print(error)
            sys.exit(1)

    def _get_authorization_header(self):
        return "Bearer " + self.get_access_token()
class AzureSentinelApi(BaseApi):
    def __init__(self):
        super().__init__()
        _, workspace_id = current_config.get_workspace()
        self._endpoint = f"{workspace_id}/providers/Microsoft.SecurityInsights/"

    def get_incidents(self, filter : str):
        """
        Gets all Azure Sentinel incidents
        """
        endpoint = f"{self._endpoint}incidents?api-version=2020-01-01&$orderby=properties/createdTimeUtc desc&$filter={filter}"
        incidents = self.get(endpoint)
        return incidents["value"]

    def get_incident(self, id : str):
        endpoint = f"{self._endpoint}incidents/{id}?api-version=2020-01-01"
        incident = self.get(endpoint)
        return incident
    
    def get_incident_alerts(self, incident_id : str):
        endpoint = f"{self._endpoint}/incidents/{incident_id}/alerts?api-version=2019-01-01-preview"
        alerts = self.post(endpoint, payload=None)
        if "value" in alerts:
            return alerts["value"]
        return []

    def get_incident_entities(self, incident_id : str):
        endpoint = f"{self._endpoint}/incidents/{incident_id}/entities?api-version=2019-01-01-preview"
        entities = self.post(endpoint, payload=None)
        if "entities" in entities:
            return entities["entities"]
        return []
        
    def get_alert(self, alert_id : str):
        analytics = AzureLogAnalytics()
        result = analytics.execute_query(f"SecurityAlert | where SystemAlertId == \"{alert_id}\"")
        alert = table_to_dict(result)
        if not alert:
            return
        return alert[0]

    def get_alert_events(self, alert_id : str):
        analytics = AzureLogAnalytics()
        alert = self.get_alert(alert_id)
        if not alert:
            return

        props_raw = alert["ExtendedProperties"]
        props = json.loads(props_raw)
        if not "Query" in props:
            return []
            
        start_time = alert["StartTime"]
        end_time = alert["EndTime"]
        result = analytics.execute_query(props["Query"], timespan=f"{start_time}/{end_time}")
        return table_to_dict(result)
        
    def get_alert_rule(self, rule_id: str):
        """
        Get alert rule by id
        """
        endpoint = f"{self._endpoint}alertRules/{rule_id}?api-version=2020-01-01"
        rule = self.get(endpoint)
        return rule

    def get_alert_rules(self):
        """
        Gets all alert rules
        """
        endpoint = f"{self._endpoint}alertRules?api-version=2020-01-01"
        alert_rules = self.get(endpoint)
        return alert_rules["value"]

    def update_alert_rule(self, rule_id : str, rule):
        endpoint = f"{self._endpoint}/alertRules/{rule_id}?api-version=2020-01-01"
        result = self.put(endpoint, rule)
        return result

    def list_alert_rule_templates(self):
        endpoint = f"{self._endpoint}/alertRuleTemplates?api-version=2020-01-01"
        result = self.get(endpoint)
        return result["value"]

    def list_data_connectors(self):
        endpoint = f"{self._endpoint}/dataConnectors?api-version=2020-01-01"
        result = self.get(endpoint)
        return result["value"]

class AzureManagementApi(BaseApi):
    def __init__(self):
        super().__init__()

    def get_subscriptions(self):
        """
        Lists all subscriptions the user has access to
        """
        subscriptions = self.get("subscriptions?api-version=2014-04-01-preview")
        return subscriptions["value"]

    def get_workspaces(self):
        """
        Lists all Log Analytics workspaces in the active subscription
        """
        _, subscription_id = current_config.get_subscription()
        workspaces = self.get(
            f"subscriptions/{subscription_id}/providers/Microsoft.OperationalInsights/workspaces?api-version=2020-08-01"
        )
        return workspaces["value"]

    def get_current_workspace(self):
        """
        Gets the currently selected workspace metadata
        """
        _, workspace_id = current_config.get_workspace()
        workspace = self.get(f"{workspace_id}?api-version=2020-08-01")
        return workspace


class AzureLogAnalytics(BaseApi):
    def __init__(self):
        super().__init__()
        _, workspace_id = current_config.get_workspace()
        self._endpoint = workspace_id

    def execute_query(self, query: str, timespan : str = None):
        data = {"query": query}
        if timespan:
            data["timespan"] = timespan

        result = self.post(f"{self._endpoint}/api/query?api-version=2020-08-01", data)
        return result

    def list_datasources(self):
        _, workspace_id = current_config.get_workspace()
        endpoint = f"{workspace_id}/dataSources?$filter=kind eq 'CustomLog'&api-version=2020-08-01"
        result = self.get(endpoint)
        return result["value"]

def table_to_dict(table_result):
    if not "Tables" in table_result:
        return

    table = table_result["Tables"][0]
    rows = []
    keys = []
    for column in table["Columns"]:
        keys.append(column["ColumnName"])

    if len(table["Rows"]) == 0:
        return dict.fromkeys(keys)
    for row in table["Rows"]:
        result_row = dict(zip(keys, row))
        rows.append(result_row)
    return rows