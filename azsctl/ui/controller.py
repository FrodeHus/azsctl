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