import msal
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    # there is a .env file which contains the values for the
    # PBI_TENANT_ID, AZURE_APP_ID, AZURE_APP_SECRET environment variables
    # you can replace os.getenv('') with your own GUID

    pbi_tenant_id = os.getenv('PBI_TENANT_ID')
    app_id = os.getenv('AZURE_APP_ID')
    app_secret = os.getenv('AZURE_APP_SECRET')

    authority_url = f'https://login.microsoftonline.com/{pbi_tenant_id}'
    scopes = [r'https://analysis.windows.net/powerbi/api/.default']

    client = msal.ConfidentialClientApplication(app_id, authority=authority_url, client_credential=app_secret)

    response = client.acquire_token_for_client(scopes)
    token = response.get('access_token')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    return headers