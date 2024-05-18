import os
import sys
import itertools
import pandas as pd
import requests
from datetime import datetime
from pathlib import Path

sys.path.insert(1, os.getcwd() + "\Python\Setup\\")

from access_token import get_access_token
from datasets import get_datasets
from workspaces import get_workspaces

headers = get_access_token()

def get_refresh_history():
    dataset_ids, dataset_names, workspace_ids = zip(*list(get_datasets()))
    dataset_workspace = zip(dataset_ids, workspace_ids)
    result = []

    for dataset_id, workspace_id in dataset_workspace:
        refresh_uri = fr"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
        response_request = requests.get(refresh_uri, headers=headers)

        if response_request.status_code == 200:
            response_text = response_request.json()['value']
            for entry in response_text:
                entry['DatasetID'] = dataset_id
                entry['WorkspaceID'] = workspace_id

            result.append(response_text)

    return list(itertools.chain(*result))


def return_final_table():
    workspace_df = pd.DataFrame.from_records(get_workspaces(), columns=['WorkspaceID', 'WorkspaceName'])
    dataset_df = pd.DataFrame.from_records(get_datasets(), columns=['DatasetID', 'DatasetName', 'WorkspaceID'])
    refresh_df = pd.DataFrame(get_refresh_history())

    columns_to_keep = ['refreshType', 'startTime', 'endTime', 'status', 'DatasetID',
                       'WorkspaceID']  #, 'serviceExceptionJson']
    capitalize_names = [name[0].capitalize() + name[1:] for name in columns_to_keep]

    refresh_df = refresh_df[columns_to_keep]
    refresh_df.columns = capitalize_names
    refresh_df['StartTime'] = pd.to_datetime(
        refresh_df['StartTime'].apply(lambda x: datetime.fromisoformat(x)).dt.strftime('%Y-%m-%d %H:%M:%S'))
    refresh_df['EndTime'] = pd.to_datetime(
        refresh_df['EndTime'].apply(lambda x: datetime.fromisoformat(x)).dt.strftime('%Y-%m-%d %H:%M:%S'))

    final_df = pd.merge(workspace_df, dataset_df, how='inner', left_on='WorkspaceID', right_on='WorkspaceID').merge(
        refresh_df, how='inner', on='WorkspaceID')
    columns_to_keep = ['WorkspaceID', 'WorkspaceName', 'DatasetID_x',
                       'DatasetName', 'RefreshType', 'StartTime', 'EndTime']  #, 'ServiceExceptionJson']
    final_df = final_df[columns_to_keep]
    final_df.rename(columns={'DatasetID_x': 'DatasetID'}, inplace=True)

    return final_df


df = return_final_table()
df.to_excel(str(Path.home()) + r"\Downloads\Refresh History.xlsx", index=False)
