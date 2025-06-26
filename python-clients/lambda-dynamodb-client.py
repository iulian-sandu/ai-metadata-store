import requests # type: ignore
import json
import argparse
import os

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
cognito_url = os.environ.get('COGNITO_URL')
cognito_scope = os.environ.get('COGNITO_SCOPE')
api_gw_url = os.environ.get('API_GW_URL')

if not all([client_id, client_secret, cognito_url, api_gw_url]):
    raise ValueError("Missing required variables")

def cognito():
    response = requests.post(f'{cognito_url}',
    data=f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope={cognito_scope}",
    headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
    return response.json()['access_token']

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {config_file} not found.")
        raise

def api_call(method, **kwargs):
    """
    Makes the API calls to the API Gateway.
    """
    auth_token = cognito()
    api_gateway = api_gw_url
    headers = {'Authorization': f'Bearer {auth_token}'}

    if method == 'get':
        account_id = kwargs['account_id']
        application_name = kwargs['application_name']
        
        response = requests.get(f'{api_gateway}/{account_id}/{application_name}', headers=headers)
        print(response.json())

    elif method == 'post':
        config_scope = kwargs['config_scope']
        json_file = kwargs['json_file']
        json_file_full_path = f'../sample-config-files/{"accounts" if config_scope == "account" else "applications"}/{json_file}'        
        json_config = load_config(json_file_full_path)

        response = requests.post(api_gateway, headers=headers, json=json_config)
        print(response.json())

def main() -> None:
    """
    Main function to handle command line arguments and call the API.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='API Gateway client inputs'
        )
    parser.add_argument('--get', help='Run get request', action='store_true')
    parser.add_argument('--account_id', help='Account ID to retrive configuration')
    parser.add_argument('--application_name', help='Application ID to retrive configuration')
    parser.add_argument('--post', help='Run post request', action='store_true')
    parser.add_argument('--config_scope', help='Scope of the config to update', choices=['account', 'application'])
    parser.add_argument('--json_file', help='JSON config file')

    args = parser.parse_args()

    if args.get:
        if not all([args.account_id, args.application_name]):
            raise ValueError("Missing required arguments")
        api_call('get', account_id=args.account_id, application_name=args.application_name)
    elif args.post:
        if not all([args.config_scope, args.json_file]):
            raise ValueError("Missing required arguments")
        api_call('post', config_scope=args.config_scope, json_file=args.json_file)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Application error: {e}")
        raise
