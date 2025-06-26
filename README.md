# AWS Lambda Hackathon - Configuration Store Engine

## Overview

**Problem statement**: As a DevOps engineer in a Cloud Platform team, managing configurations for various tools and pipelines can be challenging. These configurations are critical for providing customers access to AWS accounts and services such as Kubernetes (k8s) or GitHub Actions CI/CD pipelines.

The challenges include:
- Avoiding configuration drift and duplication
- Ensuring a centralized and scalable approach to configuration management
- Maintaining consistency across multiple environments

**Solution**: A Configuration Store Engine with AI capabilities, to provide a centralized, automated and intelligent solution for managing and interact with the configurations.

## Features and functionality

1. **AWS Cognito** - For secure authorization and authentication with client credentials, using machine to machine app client.
2. **API Gateway** - Provides two resource (```/config``` and ```/ai-chat```) for configuration management (```POST``` and ```GET```) and AI chat functionality.
3. **Lambda** - One function manages the configuration store operations, while another handles the Bedrock AI chat interaction to provide insights about the stored configurations.
4. **DynamoDB** - Stores JSON configurations as the single source of truth. Each item will get a unique version.
5. **Bedrock** - Provides AI-driven responses via an agent based on the linked Knowledge base.
6. **S3** - Stores exported configurations for Bedrock ingestion.


## Architecture
### Components

## Setup

## Usage

## Future Enhancements
