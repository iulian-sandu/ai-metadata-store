import requests # type: ignore
import json
import os

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
cognito_url = os.environ.get('COGNITO_URL')
cognito_scope = os.environ.get('COGNITO_SCOPE')
api_gw_url = os.environ.get('BEDROCK_API_GW_URL')

if not all([client_id, client_secret, cognito_url, api_gw_url]):
    raise ValueError("Missing required variables")

def cognito():
    """
    Authenticate with Cognito and return the access token.
    """
    response = requests.post(f'{cognito_url}',
    data=f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope={cognito_scope}",
    headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
    return response.json()['access_token']

def call_chat_api(prompt):
    """
    Call the Bedrock API Gateway with the given prompt and print the response.
    """
    headers = {
        'Authorization': f'Bearer {cognito()}',
        'Content-Type': 'application/json'
    }

    # Passing the same session_id keep the conversation context
    # If you want to start a new conversation, change the session_id

    data = {
        "session_id": "test-session-300",
        "prompt": prompt
    }

    response = requests.post(api_gw_url, headers=headers, json=data)
    print(response.json()['response'])

call_chat_api("What is the CICD configuration for stockexchange-api?")

# call_chat_api("What is the deployment strategy for ecommerce-api?")
# call_chat_api("Tell me the latest IAM version for the account sample-acc1-prd")
# call_chat_api("What was the previous version?")
# call_chat_api("When the latest version was applied?")