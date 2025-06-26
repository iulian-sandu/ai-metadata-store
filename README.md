# AWS Lambda Hackathon - Configuration Store Engine

## Overview

**Problem statement**: As a DevOps engineer in a Cloud Platform team, managing configurations for various tools and pipelines can be challenging. These configurations are critical for providing customers access to AWS accounts and services such as Kubernetes (k8s) or GitHub Actions CI/CD pipelines.

The challenges include:
- Avoiding configuration drift and duplication
- Ensuring a centralized and scalable approach to configuration management
- Maintaining consistency across multiple environments

**Solution**: A Configuration Store Engine with AI capabilities, to provide a centralized, automated and intelligent solution for managing and interact with the configurations.

## Features and functionality

1. Authorization and authentication, by integrating Cognito with API Gateway as an authorizer.
2. Configuration management and AI Chat

```
├── /ai-chat 
│   └── POST - Bedrock AI agent to provide AI-driven responses based on the knowledge base
└── /config
    ├── POST - Stores configurations in DynamoDB and exports them to S3
    └── /{account_id}
        └── /{application_name}
            └── GET - Retrieves configurations from DynamoDB
```

3. Agentic AI from Bedrock integrated with Knowledge base with S3 data source
4. Knowledge Base Sync - Automatically triggers ingestion of new configurations into the Bedrock knowledge base

## Architecture

![Alt text](hackathon-AWS-end2end-flow.jpeg "a title")

### Components

1. **AWS Cognito** - For secure access with client credentials, using machine to machine app client.
2. **API Gateway** - Provides two resource (```/config``` and ```/ai-chat```) for configuration management (```POST``` and ```GET```) and AI chat functionality.
3. **Lambda** - One function manages the configuration store operations, while another handles the Bedrock AI chat interaction to provide insights about the stored configurations.
4. **DynamoDB** - Stores JSON configurations as the single source of truth. Each item will get a unique version.
5. **Bedrock** - Provides AI-driven responses via an agent based on the linked Knowledge base.
6. **S3** - Stores exported configurations for Bedrock ingestion.



## Setup
Every infrastructure componenent part of the architecture diagram needs to be created and configured before using the solution. 

Resources to be created:
1. Cognito user pool with M2M app client. Export ```client_id```, ```client_secret```, ```cognito_url``` and ```cognito_scope``` as environment variables.
2. API Gateway can be imported directly using the ```hackathon-api-gw-v1-oas30-apigateway.json``` provided in the ```api-gateway-export/``` directory.
3. Two lambda functions created to handle the configurations and AI chat operations. Can be created using the functions located in the ```lambda/``` directory.
4. Set the trigger for the Lambda functions from the API Gateway based on the resources ```/config``` and ```/ai-chat```
5. Create new DynamoDB table
6. Create new S3 bucket
7. Create new Bedrock Knowledge base with S3 bucket source. 
    - First you need to request access via Model Catalog in Bedrock to amazon.titan-embed-text-v2:0 and Claude 3.5 Sonnet models.
    - Embedding model will be used to convert the JSON data into vector data to be used by the knowledge base.
8. Create new Agent in Bedrock. 
    - Setup Claude 3.5 Sonnet as a model and link the Knowledge base previously created.
    - The ```agent_alias_id```, ```agent_id``` and ```knowledge_base_id``` needs to be replaced in the Lambda Bedrock operations.

## Usage

Sample clients are located in the ```python-clients/``` directory.

### JSON Configuration management 

**POST request** (create/update configuration)

**Usecase 1**: I want to store the configuration of a new AWS account that was just created.

**Command 1**: ``` python3 ./lambda-dynamodb-client.py --post --config_scope "account" --json_file "sample-acc2-dev-account.json"  ```

**Response 1**: ``` {'statusCode': 200, 'body': '{"account_id": "33210987654", "application_name": "account-configuration", "environment": "dev", "version": "2025-06-26T18:46:14.791778", "kb_status": "started_ingestion_job"}'} ```

**Usecase 2**: I want to store the configuration of an application running in the AWS account, for CICD, k8s and Golden AMIs.

**Command 2**: ``` python3 ./lambda-dynamodb-client.py --post --config_scope "application" --json_file "sample-acc2-dev-stockexchange-api-app.json" ```

**Response 2**: ``` {'statusCode': 200, 'body': '{"account_id": "33210987654", "application_name": "stockexchange-api", "environment": "dev", "version": "2025-06-26T18:49:16.484833", "kb_status": "started_ingestion_job"}'} ```


### 2. AI chat

**Prompt**: call_chat_api("What is the CICD configuration for stockexchange-api?")

**Command**: ``` python3 ./lambda-bedrock-client.py  ```

**Response**: 
```
The CICD configuration for stockexchange-api in the development environment includes:

1. Deploy strategy: rolling
2. Pipeline type: gitlab-ci
3. Build tool: npm

This configuration suggests that the application uses a rolling deployment strategy, utilizes GitLab CI for its continuous integration and deployment pipeline, and uses npm as the build tool for managing dependencies and building the project. 
```

## Future Enhancements
