from azsctl.api import AzureSentinelApi, AzureLogAnalytics, AzureManagementApi
import asyncio

class Controller:
    def __init__(self):
        self.sentinel_api = AzureSentinelApi()
        self.log_api = AzureLogAnalytics()
        self.mgmt_api = AzureManagementApi()

    def get_alert_rules(self):
        rules = self.sentinel_api.get_alert_rules()
        return rules


class RefreshableItems:
    def __init__(self, method, method_args):
        self.retrieve = method
        self.method_args = method_args
        result = self.retrieve(*self.method_args)
        self.items = result

    def refresh(self):
        result = self.retrieve(*self.method_args)
        self.items = result