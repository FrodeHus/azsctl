from re import sub
from sentinelmon.config import Config
import requests
import json
import sys
from .auth import TokenRequester

base_url = "https://management.azure.com"
class BaseApi:
    def __init__(self, token_requester : TokenRequester):
        self._token_requester = token_requester
        self._config = Config()
    
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
        workspaces = self.get(f"subscriptions/{self._config.get(Config.SUBSCRIPTION_ID)}/providers/Microsoft.OperationalInsights/workspaces?api-version=2020-08-01")
        return workspaces

    def get_current_workspace(self):
        """
        Gets the currently selected workspace metadata
        """
        workspace = self.get(f"{self._config.get(Config.WORKSPACE_ID)}?api-version=2020-08-01")
        return workspace
