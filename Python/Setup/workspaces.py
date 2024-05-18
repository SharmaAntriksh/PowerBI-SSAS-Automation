import requests
from access_token import get_access_token

headers = get_access_token()


def get_workspaces():

    workspace_uri = 'https://api.powerbi.com/v1.0/myorg/groups?$filter=(isOnDedicatedCapacity eq true)'
    # workspace_uri = 'https://api.powerbi.com/v1.0/myorg/groups'
    response_request = requests.get(workspace_uri, headers=headers)
    result = response_request.json()

    workspace_id = [workspace['id'] for workspace in result['value']]
    workspace_name = [workspace['name'] for workspace in result['value']]

    return zip(workspace_id, workspace_name) 