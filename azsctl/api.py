from azsctl import current_config
import requests
import sys
from .auth import TokenRequester

base_url = "https://management.azure.com"
class BaseApi:
    def __init__(self):
        self._token_requester = TokenRequester()
    
    def get_access_token(self):
        token = self._token_requester.acquire_token()
        return token
    
    def get(self, path : str):
        try:
            result = requests.get(f"{base_url}/{path}", headers={
                'Authorization': 'Bearer ' + self.get_access_token()
            }).json()
            return result
        except Exception as error:
            print(error)
            sys.exit(1)

    def post(self, path : str, payload : any):
        try:
            result = requests.post(f"{base_url}/{path}", data=payload,
            headers={
                'Authorization': 'Bearer ' + self.get_access_token()
            })
        except Exception as error:
            print(error)
            sys.exit(1)
class AzureSentinelApi(BaseApi):
    def __init__(self):
        super().__init__()
        _, workspace_id = current_config.get_workspace()
        self._endpoint = f"{workspace_id}/providers/Microsoft.SecurityInsights/"   
    
    def get_incidents(self):
        """
        Gets all Azure Sentinel incidents
        """
        endpoint = f"{self._endpoint}incidents?api-version=2020-01-01"
        incidents = self.get(endpoint)
        return incidents["value"]
    
    def get_alert_rules(self):
        """
        Gets all alert rules
        """
        endpoint = f"{self._endpoint}alertRules?api-version=2020-01-01"
        alert_rules = self.get(endpoint)
        return alert_rules["value"]

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
        workspaces = self.get(f"subscriptions/{subscription_id}/providers/Microsoft.OperationalInsights/workspaces?api-version=2020-08-01")
        return workspaces["value"]

    def get_current_workspace(self):
        """
        Gets the currently selected workspace metadata
        """
        _, workspace_id = current_config.get_workspace()
        workspace = self.get(f"{workspace_id}?api-version=2020-08-01")
        return workspace["value"]

class AzureLogAnalytics(BaseApi):
    def __init__(self):
        super().__init__()

    def execute_query(self, query : str):
        pass