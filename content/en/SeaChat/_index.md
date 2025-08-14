---
title: SeaChat API Wiki
linkTitle: SeaChat API
type: docs
menu: {main: {weight: 10}}
---

## Overview

SeaChat API is a comprehensive solution for creating and managing intelligent conversational agents (bots) within your workspace. This API enables you to build sophisticated chatbots that can handle customer service, sales, marketing, and various other use cases with advanced natural language processing capabilities.

The SeaChat platform provides a robust foundation for developing conversational AI applications that can understand context, maintain conversation history, and provide intelligent responses based on uploaded knowledge bases. Whether you're building a customer support bot, a sales assistant, or an educational chatbot, SeaChat API offers the tools and flexibility needed to create engaging conversational experiences.

## Key Features

### Agent Management
SeaChat API provides comprehensive agent management capabilities that allow you to create, configure, update, and delete conversational agents within your workspace. Each agent can be customized with specific use cases, response languages, and behavioral parameters to match your business requirements.

The agent management system supports multiple use cases including Customer Service, Sales, Marketing, HR, IT Support, Education, Healthcare, Finance, Legal, and Other custom applications. This flexibility ensures that you can tailor your conversational agents to meet specific industry needs and business objectives.

### Knowledge Base Integration
One of the most powerful features of SeaChat API is its knowledge base integration capability. You can upload various types of documents and files that serve as the foundation for your agent's knowledge and responses. The system processes these files and creates a searchable knowledge base that your agent can reference when responding to user queries.

The knowledge base import process is asynchronous, allowing you to upload large volumes of content without blocking other operations. The API provides status tracking mechanisms so you can monitor the progress of knowledge base imports and receive notifications when the process is complete.

### Conversation Handling
SeaChat API excels at managing conversations and message exchanges between users and agents. The conversation management system maintains context across multiple interactions, ensuring that your agent can provide coherent and relevant responses throughout extended conversations.

Each conversation is uniquely identified and can be retrieved, updated, or analyzed using the API endpoints. This enables you to build sophisticated conversation flows, implement conversation analytics, and provide personalized experiences based on conversation history.

### Real-time Messaging
The API supports real-time messaging capabilities that enable immediate exchange of messages between users and agents. This real-time functionality is essential for creating responsive conversational experiences that feel natural and engaging to users.

Messages can include various types of content and can be sent and received through multiple channels. The messaging system maintains message history and provides delivery confirmation to ensure reliable communication.

### Webhook Support
SeaChat API includes comprehensive webhook support that allows you to implement real-time notifications and integrations with external systems. Webhooks can be configured to receive notifications about various events, including message delivery, conversation updates, and knowledge base import completion.

This webhook functionality enables you to build sophisticated integrations that can trigger actions in external systems based on conversational events, creating seamless workflows between your chatbot and other business applications.

## Getting Started

### Prerequisites

Before you can begin using the SeaChat API, you need to complete several important setup steps that will provide you with the necessary credentials and workspace configuration.

#### Workspace Creation
The first step is to create a workspace in SeaChat. Your workspace serves as the container for all your agents, conversations, and knowledge bases. When you create a workspace, you'll receive a unique workspace ID that you'll need for all API calls.

To find your workspace ID, navigate to your SeaChat dashboard and look at the URL structure, which follows this format: `https://chat.seasalt.ai/gpt/workspace/{workspace-id}/bot/{bot-id}/`. The workspace ID is the alphanumeric string that appears in the workspace-id position of the URL.

#### API Key Generation
Once you have a workspace, you need to obtain an API key for authentication. Navigate to the "API Key" tab under the "Workspace" dropdown in the SeaChat interface. Click the `Generate API Key` button to generate a new API key for your workspace.

Your API key is a sensitive credential that provides access to your workspace and all associated data. Protect this key carefully and never share it publicly or include it in client-side code. If you suspect your API key has been compromised, you can click the "refresh" icon to deactivate the old key and generate a new one.

#### Authentication Setup
All API requests must include proper authentication using Bearer token authentication. Your API key serves as the bearer token and must be included in the Authorization header of every request to the SeaChat API.

### Basic Workflow

The typical workflow for using SeaChat API involves several key steps that build upon each other to create a fully functional conversational agent.

#### Create an Agent
The first step in the workflow is to create a new agent using the `POST /api/v1/public/bots` endpoint. When creating an agent, you'll specify important configuration parameters including the agent's name, description, intended use case, and default response language.

The agent creation process establishes the foundation for your conversational AI, setting up the basic parameters that will govern how your agent behaves and responds to user interactions. You can specify whether the agent should support live agent transfer, which enables seamless handoff to human operators when needed.

#### Import Knowledge Base
After creating your agent, the next crucial step is to upload knowledge base files using the `POST /api/v1/public/bots/{bot_id}/kb/import` endpoint. This process involves uploading documents, files, or other content that will serve as the source of knowledge for your agent's responses.

The knowledge base import is an asynchronous process that may take some time to complete, depending on the volume and complexity of the content being processed. The API returns a task ID that you can use to monitor the progress of the import operation.

#### Monitor Import Status
Since knowledge base import is asynchronous, you should implement monitoring to track the progress of the import operation. Use the task ID returned from the import request to periodically check the status using the appropriate status endpoint.

You can also implement a callback URL that will receive notifications when the import process completes. This approach is more efficient than polling and ensures that you're notified immediately when your knowledge base is ready for use.

#### Start Conversations
Once your agent is created and the knowledge base is imported, you can begin creating conversations using the `POST /api/v1/public/bots/{bot_id}/conversations/ops/get_or_create` endpoint. This endpoint either retrieves an existing conversation or creates a new one based on the user information provided.

Each conversation is associated with a specific user and maintains its own context and message history. This enables your agent to provide personalized responses and maintain coherent conversations across multiple interactions.

#### Send and Receive Messages
With conversations established, you can exchange messages using the `POST /api/v1/public/bots/{bot_id}/conversations/{conversation_id}/messages` endpoint. This endpoint allows you to send user messages to the agent and receive intelligent responses based on the agent's knowledge base and configuration.

The messaging system maintains full message history and provides detailed information about each message, including timestamps, sender information, and message content. This enables you to build sophisticated conversation analytics and user experience optimization.

## Authentication

All interactions with the SeaChat API require proper authentication using Bearer token authentication. This security mechanism ensures that only authorized applications and users can access your workspace and agent data.

### Bearer Token Authentication

Every API request must include an Authorization header with your API key formatted as a Bearer token. The header format is:

```
Authorization: Bearer [your-access-token]
```

Replace `[your-access-token]` with the actual API key you obtained from your SeaChat workspace settings. This token provides full access to your workspace, so it should be treated as a sensitive credential.

### Example Authentication

Here's an example of how to include authentication in a cURL request:

```bash
curl -X 'POST' \
  'https://chat.seasalt.ai/api/v1/public/bots' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [your-access-token]' \
  -H 'Content-Type: application/json' \
  -d '{
    "workspace_id": "your-workspace-id",
    "name": "My SeaChat Agent",
    "description": "An intelligent customer service agent",
    "use_case": "Customer Service",
    "live_agent_transfer": false,
    "default_response_language": "default",
    "is_enabled": true
  }'
```

## API Endpoints

### Agent Management Endpoints

#### Create Agent
- **Endpoint**: `POST /api/v1/public/bots`
- **Purpose**: Creates a new conversational agent in your workspace
- **Required Parameters**: workspace_id, name
- **Optional Parameters**: description, use_case, live_agent_transfer, default_response_language, is_enabled

#### Get Agent List
- **Endpoint**: `GET /api/v1/public/bots`
- **Purpose**: Retrieves a list of all agents in your workspace
- **Parameters**: workspace_id, offset, limit, order_by

#### Get Agent by ID
- **Endpoint**: `GET /api/v1/public/bots/{bot_id}`
- **Purpose**: Retrieves detailed information about a specific agent
- **Parameters**: bot_id

#### Update Agent
- **Endpoint**: `PUT /api/v1/public/bots/{bot_id}`
- **Purpose**: Updates the configuration of an existing agent
- **Parameters**: bot_id, plus any fields to update

#### Delete Agent
- **Endpoint**: `DELETE /api/v1/public/bots/{bot_id}`
- **Purpose**: Permanently deletes an agent and all associated data
- **Parameters**: bot_id

### Knowledge Base Endpoints

#### Import Knowledge Base
- **Endpoint**: `POST /api/v1/public/bots/{bot_id}/kb/import`
- **Purpose**: Uploads files to create or update the agent's knowledge base
- **Parameters**: bot_id, files (multipart/form-data), callback_url (optional)

#### Get Import Status
- **Endpoint**: `GET /api/v1/public/bots/{bot_id}/kb/import/status/{task_id}`
- **Purpose**: Checks the status of a knowledge base import operation
- **Parameters**: bot_id, task_id

#### Get Knowledge Base Files
- **Endpoint**: `GET /api/v1/public/bots/{bot_id}/kb/files`
- **Purpose**: Retrieves a list of files in the agent's knowledge base
- **Parameters**: bot_id, offset, limit, order_by

#### Delete Knowledge Base File
- **Endpoint**: `DELETE /api/v1/public/bots/{bot_id}/kb/files/{file_id}`
- **Purpose**: Removes a specific file from the agent's knowledge base
- **Parameters**: bot_id, file_id

### Conversation Management Endpoints

#### Get or Create Conversation
- **Endpoint**: `POST /api/v1/public/bots/{bot_id}/conversations/ops/get_or_create`
- **Purpose**: Retrieves an existing conversation or creates a new one for a user
- **Parameters**: bot_id, user (object with id, first_name, last_name)

#### Get Messages
- **Endpoint**: `GET /api/v1/public/bots/{bot_id}/conversations/{conversation_id}/messages`
- **Purpose**: Retrieves message history for a specific conversation
- **Parameters**: bot_id, conversation_id, offset, limit, order_by

#### Send Message
- **Endpoint**: `POST /api/v1/public/bots/{bot_id}/conversations/{conversation_id}/messages`
- **Purpose**: Sends a message in a conversation and receives the agent's response
- **Parameters**: bot_id, conversation_id, content

## Response Codes and Error Handling

### Success Response Codes

SeaChat API uses two primary response codes to indicate successful operations:

- **200 OK**: The operation was successful and includes a response body with the requested data or confirmation of the action performed.
- **204 No Content**: The operation was successful but does not include a response body. This is typically used for delete operations or other actions that don't require returning data.

### Error Response Format

When an error occurs (response code 400 or higher), the API returns a standardized error response format that provides detailed information about what went wrong. The error response includes three key components:

- **detail**: A human-readable description of the error that occurred
- **code**: A numeric error code that can be used programmatically to identify the specific type of error
- **parameters**: An object containing additional context about the error, such as the specific parameters that caused the issue

### Example Error Response

```json
{
    "detail": "The token: testtoken decoding failed.",
    "code": 40007,
    "parameters": {
        "token": "testtoken"
    }
}
```

### Common Error Scenarios

#### Authentication Errors
- **Code 40007**: Token decoding failed - indicates an invalid or malformed API key
- **Code 401**: Unauthorized - API key is missing or invalid
- **Code 403**: Forbidden - API key doesn't have permission for the requested operation

#### Validation Errors
- **Code 422**: Validation Error - request parameters don't meet the required format or constraints
- **Code 400**: Bad Request - malformed request or missing required parameters

#### Resource Errors
- **Code 404**: Not Found - the requested resource (agent, conversation, etc.) doesn't exist
- **Code 409**: Conflict - operation conflicts with current resource state

## Best Practices

### Security Best Practices

#### API Key Management
Treat your API keys as sensitive credentials and implement proper security measures to protect them. Never include API keys in client-side code, public repositories, or any location where they might be exposed to unauthorized users.

Store API keys securely using environment variables, secure configuration management systems, or dedicated secret management services. Implement key rotation policies and monitor API key usage for any suspicious activity.

#### Access Control
Implement proper access control mechanisms in your applications to ensure that only authorized users and systems can trigger API calls. Use role-based access control and principle of least privilege to limit access to only what's necessary for each user or system component.

### Performance Best Practices

#### Rate Limiting
Respect API rate limits to avoid service disruption and ensure optimal performance for all users. Implement exponential backoff strategies for handling rate limit responses and consider implementing client-side rate limiting to prevent exceeding API limits.

Monitor your API usage patterns and optimize your application's API call frequency to stay within reasonable limits while maintaining good user experience.

#### Asynchronous Operations
Take advantage of asynchronous operations, particularly for knowledge base imports and other long-running processes. Implement proper status monitoring and callback mechanisms to handle asynchronous operations efficiently without blocking your application.

#### Caching Strategies
Implement appropriate caching strategies for data that doesn't change frequently, such as agent configura
(Content truncated due to size limit. Use line ranges to read in chunks)

{{% pageinfo %}}
This is a placeholder page that shows you how to use this template site.
{{% /pageinfo %}}

This section is where the user documentation for your project lives - all the
information your users need to understand and successfully use your project.

For large documentation sets we recommend adding content under the headings in
this section, though if some or all of them don’t apply to your project feel
free to remove them or add your own. You can see an example of a smaller Docsy
documentation site in the [Docsy User Guide](https://docsy.dev/docs/), which
lives in the [Docsy theme
repo](https://github.com/google/docsy/tree/master/userguide) if you'd like to
copy its docs section.

Other content such as marketing material, case studies, and community updates
should live in the [About](/about/) and [Community](/community/) pages.

Find out how to use the Docsy theme in the [Docsy User
Guide](https://docsy.dev/docs/). You can learn more about how to organize your
documentation (and how we organized this site) in [Organizing Your
Content](https://docsy.dev/docs/best-practices/organizing-content/).
