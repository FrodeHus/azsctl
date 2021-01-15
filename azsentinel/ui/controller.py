from azsentinel.api import AzureSentinelApi, AzureLogAnalytics, AzureManagementApi
import asyncio
class Controller:
    def __init__(self):
        self.async_loop = asyncio.get_event_loop()
        self.sentinel_api = AzureSentinelApi()
        self.log_api = AzureLogAnalytics()
        self.mgmt_api = AzureManagementApi()

    def get_alert_rules(self):
        rules = self.sentinel_api.get_alert_rules()
        return rules

    def get_incidents(self):
        incidents = self.sentinel_api.get_incidents("properties/status ne 'Closed'")
        return incidents


