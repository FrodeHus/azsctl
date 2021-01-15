from azsentinel.api import AzureSentinelApi


def get_alert(id: str):
    api = AzureSentinelApi()
    return api.get_alert(id)


def get_alert_events(id: str):
    api = AzureSentinelApi()
    return api.get_alert_events(id)