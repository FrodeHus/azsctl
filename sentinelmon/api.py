from sentinelmon import current_config
import requests
import sys
from .auth import TokenRequester

base_url = "https://management.azure.com"
class BaseApi:
    def __init__(self, token_requester : TokenRequester):
        self._token_requester = token_requester
    
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

class AzureSentinelApi(BaseApi):
    def __init__(self, token_requester : TokenRequester):
        super().__init__(token_requester)        
    
    def get_incidents(self):
        """
        Gets all Azure Sentinel incidents
        """
        _, workspace_id = current_config.get_workspace()
        endpoint = f"{workspace_id}/providers/Microsoft.SecurityInsights/incidents?api-version=2020-01-01"
        incidents = self.get(endpoint)
        return incidents

class AzureManagementApi(BaseApi):
    def __init__(self, token_requester : TokenRequester):
        super().__init__(token_requester)
        self._token_requester = token_requester

    def get_subscriptions(self):
        """
        Lists all subscriptions the user has access to
        """
        subscriptions = self.get("subscriptions?api-version=2014-04-01-preview")
        return subscriptions

    def get_workspaces(self):
        """
        Lists all Log Analytics workspaces in the active subscription
        """
        _, subscription_id = current_config.get_subscription()
        workspaces = self.get(f"subscriptions/{subscription_id}/providers/Microsoft.OperationalInsights/workspaces?api-version=2020-08-01")
        return workspaces

    def get_current_workspace(self):
        """
        Gets the currently selected workspace metadata
        """
        _, workspace_id = current_config.get_workspace()
        workspace = self.get(f"{workspace_id}?api-version=2020-08-01")
        return workspace
