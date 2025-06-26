import json
import boto3 # type: ignore
from botocore.exceptions import ClientError # type: ignore

def invoke_agent(prompt, session_id):
    """
    Invokes a Bedrock agent with the given prompt and session ID.
    Returns the response from the agent.
    """
    bedrock = boto3.client('bedrock-agent-runtime', region_name='eu-central-1')
    agent_alias_id = 'NRGINMOGR2'
    agent_id = 'J2XJOWR6WL'
    knowledge_base_id = 'AVMGXIX4FG'
    number_of_results = 30

    response = bedrock.invoke_agent(
        agentAliasId=agent_alias_id,
        agentId=agent_id,
        sessionId=session_id,
        sessionState = {
            "knowledgeBaseConfigurations":  [{
                "knowledgeBaseId": knowledge_base_id,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": number_of_results,
                    }
                }
            }]
        },
        inputText=prompt
    )

    completion = ""
    for event in response.get("completion"):
            chunk = event["chunk"]
            completion = completion + chunk["bytes"].decode()
    
    return completion


def lambda_handler(event, context):
    """
    Lambda function to handle the API Gateway requests
    """
    try:
        prompt = event['body'].get('prompt', '')
        session_id = event['body'].get('session_id', '')

        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Prompt is required'})
            }
        
        response = invoke_agent(prompt, session_id)

        return {
            'statusCode': 200,
            'response': response
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Bedrock error: {str(e)}'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal error: {str(e)}'})
        }
