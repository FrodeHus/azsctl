from azsentinel.api import AzureLogAnalytics

def execute_query(kql : str):
    api = AzureLogAnalytics()
    result = api.execute_query(kql)
    if not "Tables" in result:
        return

    table = result["Tables"][0]
    rows = []
    keys = []
    for column in table["Columns"]:
        keys.append(column["ColumnName"])

    if len(table["Rows"]) == 0:
        return dict.fromkeys(keys)
    for row in table["Rows"]:
        result_row = dict(zip(keys, row))
        rows.append(result_row)
    return rows

def list_datasources():
    api = AzureLogAnalytics()
    return api.list_datasources()