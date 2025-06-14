import msal
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token():

    # there is a .env file which contains the values for the
    # PBI_TENANT_ID, CLIENT_ID, CLIENT_SECRET environment variables
    # you can replace os.getenv('') with your own GUID

    # To create .env with PowerShell:
    # @"
    # PBI_TENANT_ID ='443c483'
    # CLIENT_ID ='f5fbda3'
    # CLIENT_SECRET ='p-88aBf'
    # "@ | Set-Content "TargetFolderPath\.env"


    pbi_tenant_id = os.getenv('PBI_TENANT_ID')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    authority_url = f'https://login.microsoftonline.com/{pbi_tenant_id}'
    scopes = [r'https://analysis.windows.net/powerbi/api/.default']

    client = msal.ConfidentialClientApplication(
        client_id = client_id, 
        authority = authority_url, 
        client_credential = client_secret
    )

    response = client.acquire_token_for_client(scopes)
    token = response.get('access_token')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    return headers