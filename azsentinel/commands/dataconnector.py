from azsentinel.api import AzureSentinelApi

def list_data_connectors():
    api = AzureSentinelApi()
    return api.list_data_connectors()