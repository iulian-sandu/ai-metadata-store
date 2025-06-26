import boto3 # type: ignore
from boto3.dynamodb.conditions import Key, Attr # type: ignore
import datetime
import json
from time import sleep

def dynamodb():
    """
    Returns a DynamoDB resource for the 'ai-metadata-store' table.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ai-metadata-store')
    
    return table

def insert_configuration(event) -> dict:
    """
    Inserts a new configuration into the DynamoDB table, push the file to S3.
    Starts an ingestion job in Bedrock.
    """
    version = datetime.datetime.now().isoformat()
    table = dynamodb()

    account_id = event['body-json']['account_id']
    application_name = event['body-json']['application']
    environment = event['body-json']['environment']
    config = event['body-json']['config']

    item = {
        'account_id': account_id,
        'application_name': application_name,
        'environment': environment,
        'config': config,
        'version': version
    }

    table.put_item(Item=item)

    sleep(5)

    latest_only = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id),
        FilterExpression=Attr('application_name').eq(application_name),
        ConsistentRead=True,
        ScanIndexForward=False,
        Limit=1
    )

    latest_version = latest_only['Items'][0]['version']

    # Save the latest configuration to a json file in S3
    # This will be used by the AI Metadata Store Knowledge Base in Bedrock

    for item in latest_only['Items']:
        s3_bucket = 'ai-metadata-store-kb-files'
        s3_config_key = f'{latest_version}-{account_id}-{application_name}.json'

        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_config_key,
            Body=json.dumps(item, indent=4),
            ContentType='application/json'
        )

    # Start the ingestion job in Bedrock to sync the knowledge base

    kb_status = bedrock()

    return  {
        'statusCode': 200,
        'body': json.dumps({
            'account_id': account_id,
            'application_name': application_name,
            'environment': environment,
            'version': latest_version,
            'kb_status': "started_ingestion_job"
        })
    }

def bedrock() -> dict:
    """
    Sync the knowledge base in Bedrock
    """
    bedrock = boto3.client('bedrock-agent', region_name='eu-central-1')

    # Sync data source for the knowledge base
    response = bedrock.start_ingestion_job(
        dataSourceId='VWYBHWL0RL',
        description='Sync knowledge base in Bedrock for new item dummy-name',
        knowledgeBaseId='AVMGXIX4FG'
    )

    return response

def get_configuration(account_id: str, application_name: str) -> dict:
    """
    Retrieves the configuration for a given account and application.
    """
    table = dynamodb()
    latest_only = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id),
        FilterExpression=Attr('application_name').eq(application_name),
        ConsistentRead=True,
        ScanIndexForward=False
    )

    if latest_only['Items'] == []:
        return {'statusCode': 404, 'body': 'No configuration found.'}

    for item in latest_only['Items']:
        return item
    
def lambda_handler(event, context):
    """
    Lambda function to handle the API Gateway requests
    """
    api_method = event['http-method']

    if api_method == 'GET':
        return get_configuration(event['account_id'], event['application_name'])
    elif api_method == 'POST':
        return insert_configuration(event)
