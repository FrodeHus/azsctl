from azsctl.api import AzureLogAnalytics

def execute_query(kql : str):
    api = AzureLogAnalytics()
    return api.execute_query(kql)