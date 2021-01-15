from azsentinel.api import AzureManagementApi
def show_workspace():
    api = AzureManagementApi()
    return api.get_current_workspace()

def list_workspaces():
    api = AzureManagementApi()
    return api.get_workspaces()