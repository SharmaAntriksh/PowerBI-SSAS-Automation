import requests
import access_token
import workspaces

headers = access_token.get_access_token()


def get_datasets(workspace_id=None):
    if workspace_id is None:
        all_workspaces = workspaces.get_workspaces()
    else:
        all_workspaces = [workspace_id]

    dataset_ids = []
    dataset_names = []
    workspace_ids = []

    for workspace_id, workspace_name in all_workspaces:

        dataset_uri = fr"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"
        response_request = requests.get(dataset_uri, headers=headers)
        result = response_request.json()

        for item in result['value']:
            dataset_ids.append(item['id'])
            dataset_names.append(item['name'])
            workspace_ids.append(workspace_id)

    return zip(dataset_ids, dataset_names, workspace_ids)