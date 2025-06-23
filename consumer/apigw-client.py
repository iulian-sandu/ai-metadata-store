import requests # type: ignore
import json

# Get Cognito token
client_id = ""
client_secret = ""
cognito_url = ""
api_gw_url = ""

def cognito():
    response = requests.post(f'{cognito_url}',
    data=f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=default-m2m-resource-server-n6dl76/read",
    headers={'Content-Type': 'application/x-www-form-urlencoded'})

    return response.json()['access_token']

def api_call():
    auth_token = cognito()
    api_gateway = api_gw_url
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(api_gateway, headers=headers)

    return response.json()


def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

json_config = load_config('config.json')

data = {
    "account_id": "XXX",
    "account_name": "John Doe",
    "account_email": "john.doe@example.com",
    "payload": {
        "config": json_config
    }
}

response = requests.post(api_gw_url,headers=headers, data=json.dumps(data))

