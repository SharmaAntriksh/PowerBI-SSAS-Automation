import os
import sys
import requests
import pandas as pd

sys.path.insert(1, os.getcwd() + r"\Python\Setup\\")

from access_token import get_access_token

headers  =  get_access_token()


def execute_query(workspace_id, dataset_id, dax_query):
    
    dax_query_payload = {
        "queries": [
            {
                "query": f'{dax_query}'
            }
        ],
        "serializerSettings": {
            "includeNulls": True
        }
    }


    query_url  = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/executeQueries'
    response = requests.post(query_url, json = dax_query_payload, headers = headers)
    result = response.json()['results'][0]['tables'][0]['rows']
    df = pd.DataFrame.from_dict(result)

    return df


dax_query = """
    DEFINE 
        MEASURE Sales[Cost Amount] = 
            SUMX ( Sales, Sales[Quantity] * Sales[Unit Cost] )
    EVALUATE 
        VAR CustomerSales = 
            ADDCOLUMNS ( 
                ALL ( Customer[CustomerKey], Customer[Name] ),
                "Sales", [Sales Amount],
                "Cost", [Cost Amount]
            )
        VAR TopCustomersBySales = 
            TOPN ( 10, CustomerSales, [Sales], DESC )
        RETURN
            TopCustomersBySales
"""


workspace_id = '119474-####'
dataset_id = '045531-#####'

dax_query_result =  execute_query(workspace_id, dataset_id, dax_query)

print(dax_query_result)