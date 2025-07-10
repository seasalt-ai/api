---
title: Seasalt.ai Webhook Notification API Tutorial
linkTitle: Webhook Notification API Tutorial
description:
  Learn how to use Seasalt.ai's Webhook Notification API to receive real-time
  event updates for conversations, calls, and user actions. Ideal for
  integrations with Zapier and custom automation workflows.

type: docs
weight: 1
---

## Overview

A webhook-based notification system that lets your services receive real-time
updates from Seasalt.ai products like SeaChat. Whether you want to track new
conversations, missed calls, or contact changes, using the following endpoints
ensures you stay informed the moment it happens. With support for multiple event
types and delivery modes (immediate, delayed, batched), Portal's Webhook
Notification are ideal for diverse automation and integration needs. You can
also access the RESTful API docs of Webhook Notification
[here](./Docs/notify-api/)

One powerful use case built on top of this webhook system is our Zapier
integration. When an event is emitted via webhook, it can immediately trigger a
Zap, allowing users to seamlessly connect Seasalt.ai products with tools like
Google Sheets, Notion, Slack, and more. In this setup, webhooks act as the
upstream event source, and Zapier serves as the downstream automation engine,
consuming those events and turning them into custom workflows without any code.
Explore the integration here:
[Seasalt.ai on Zapier](https://zapier.com/apps/seasaltai/integrations)

---

## Prerequisites

Ensure the following are in place:

### **1\. Generate Your API Key**

All APIs require a valid API key issued from your workspace. All requests must
include a valid API key in the request header (`X-API-Key`).

- Go to **Settings → API Key** tab.

- Click **Add New Key** and check `SeaNotify` as the scope.

- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

### **2\. Prepare Your Webhook Receiver**

Your server must:

- Be publicly accessible over **HTTPS**

- Accept **POST** requests

- Handle **application/json** payloads

---

## Subscription APIs

This section explains how to manage webhook subscriptions in your workspace.

### **Create a Subscription**

Create a new webhook subscription in your Portal workspace.

#### Endpoint

`POST https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription`

Use this endpoint to register a webhook that will receive event notifications
from Portal.

#### Authorization

You must provide your API key in the `X-API-KEY` header.

#### Request Body

| Field         | Type              | Required | Description                                                           |
| ------------- | ----------------- | -------- | --------------------------------------------------------------------- |
| `webhook_url` | `string`          | ✅       | The publicly accessible URL to receive webhook events.                |
| `event_types` | `array of string` | ✅       | List of event types to subscribe to. See supported event types below. |
| `created_by`  | `string`          |          | Identifier of the user creating the subscription.                     |
| `is_enabled`  | `boolean`         | ✅       | Whether the subscription is active (`true`) or paused (`false`).      |
| `type`        | `string`          |          | Subscription source. Options: `"SEASALT"` (default), `"ZAPIER"`       |

**Supported Event Types**

To get a list of supported event types, you can use
[this endpoint](#get-a-list-of-supported-events).

Once you've subscribed to the desired event_types, refer to the
[Event Payload Schema Reference section](#event-payload-schema-reference) for
detailed information on the structure of each event’s webhook payload. This
helps you understand what fields to expect and how to process them correctly in
your application.

- `conversation.new`
- `conversation.updated`
- `message.new`
- `conversation.label.added`
- `conversation.label.deleted`
- `conversation.ended`
- `call.new`
- `call.updated`
- `call.ended`

**Sample Request**

```bash
curl -X POST "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://api.example.com/webhook",
    "event_types": ["conversation.new", "message.new"],
    "created_by": "user_12345",
    "is_enabled": true,
    "type": "SEASALT"
  }'
```

**Sample Successful Response**

```bash
{
  "webhook_url": "https://api.example.com/webhook",
  "event_types": [
    "conversation.new",
    "message.new"
  ],
  "created_by": "user_12345",
  "is_enabled": true,
  "type": "SEASALT"
}
```

### **Retrieve a Subscription**

This endpoint retrieves the details of a specific webhook subscription by its
ID.

#### Endpoint

`GET https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

You must provide your API key in the `X-API-KEY` header.

**Sample Request**

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>"
```

**Sample Successful Response**

```bash
{
  "webhook_url": "https://api.example.com/webhook",
  "event_types": [
    "conversation.new",
    "message.new"
  ],
  "created_by": "user_12345",
  "is_enabled": true,
  "type": "SEASALT"
}
```

### Retrieve a List of Subscriptions based on criterion

#### Endpoint

`GET https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Query Parameter

We support the following optional queries to retrieve subscriptions. If not
provided, all subscriptions for the workspace will be returned.

| Name       | Type   | Required | Default           | Description                                                   |
| ---------- | ------ | -------- | ----------------- | ------------------------------------------------------------- |
| `order_by` | string |          | `created_at:desc` | Order items by field and direction. Format: `field:direction` |
| `type`     | string |          |                   | Filter by subscription type. Enum: `SEASALT`, `ZAPIER`        |

_Order By Options_

The `order_by` query parameter allows you to sort the delivery logs by a
specific field and direction.  
The format is `field:direction`, where direction can be either `asc` for
ascending or `desc` for descending.

**Supported fields for Order By:**

| `order_by` Value  | Description                                 |
| ----------------- | ------------------------------------------- |
| `created_at:asc`  | Oldest subscriptions first                  |
| `created_at:desc` | Newest subscriptions first (default)        |
| `updated_at:asc`  | Least recently updated subscriptions first  |
| `updated_at:desc` | Most recently updated subscriptions first   |
| `id:asc`          | Sort by subscription ID (A–Z)               |
| `id:desc`         | Sort by subscription ID (Z–A)               |
| `created_by:asc`  | Creator A–Z                                 |
| `created_by:desc` | Creator Z–A                                 |
| `updated_by:asc`  | Last updater A–Z                            |
| `updated_by:desc` | Last updater Z–A                            |
| `is_enabled:asc`  | Inactive subscriptions first                |
| `is_enabled:desc` | Active subscriptions first                  |
| `type:asc`        | Subscription type A–Z (`SEASALT`, `ZAPIER`) |
| `type:desc`       | Subscription type Z–A                       |

If not specified, the default is `created_at:desc`.

**Sample Request**

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription?order_by=created_at:asc&type=SEASALT" \
  -H "X-API-KEY: <your_api_key>"
```

**Sample Successful Response**

```bash
{
  "subscriptions": [
    {
      "webhook_url": "https://api.example.com/webhook",
      "event_types": [
        "conversation.new",
        "message.new"
      ],
      "created_by": "user_12345",
      "is_enabled": true,
      "type": "SEASALT",
      "id": "sub_12345",
      "created_at": "2024-03-10T15:30:00Z",
      "updated_at": "2024-03-10T15:30:00Z",
      "updated_by": "user_12345"
    }
  ]
}

```

### **Update a Subscription**

Modify an existing webhook subscription to update its webhook URL, event types,
status, or type.

#### Endpoint

`PATCH https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Field       | Type     | Required | Description                                        |
| ----------- | -------- | -------- | -------------------------------------------------- |
| webhook_url | string   | No       | The URL to which webhook events will be delivered. |
| event_types | string[] | No       | A list of event types you want to subscribe to.    |
| is_enabled  | boolean  | No       | Whether the subscription is active.                |
| type        | string   | No       | Type of subscription. Enum: `SEASALT`, `ZAPIER`.   |
| updated_by  | string   | Yes      | Email or identifier of the user making the update. |

**Sample Request**

```bash
curl -X PATCH "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://api.example.com/webhook",
    "event_types": ["conversation.new", "message.new"],
    "updated_by": "user_12345",
    "is_enabled": true
  }'

```

**Sample Successful Response**

```bash
{
  "webhook_url": "https://api.example.com/webhook",
  "event_types": [
    "conversation.new",
    "message.new"
  ],
  "created_by": "user_12345",
  "is_enabled": true,
  "type": "SEASALT",
  "id": "sub_12345",
  "created_at": "2024-03-10T15:30:00Z",
  "updated_at": "2024-03-10T15:30:00Z",
  "updated_by": "user_12345"
}

```

### **Remove a Subscription**

Delete an existing webhook subscription from your workspace. This action
permanently disables event delivery to the specified webhook URL.

#### Endpoint

`DELETE https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

**Sample Request**

```bash
curl -X DELETE "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>"
```

**Sample Request**

HTTP Status Code: 204 No Content

## **Get a List of Supported Events**

Retrieve a list of all event types that can be used when creating or updating
webhook subscriptions. Each event type includes a brief description of when it
is triggered.

#### Endpoint

`GET https://portal.seasalt.ai/notify/api/v1/event_types`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

**Sample Request**

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/event_types" \
  -H "X-API-KEY: <your_api_key>"
```

**Sample Successful Response**

```bash
[
  {
    event_type: 'conversation.new',
    description: 'Triggered when a new conversation is created',
  },
  {
    event_type: 'conversation.updated',
    description: 'Triggered when a conversation is updated',
  },
  {
    event_type: 'message.new',
    description: 'Triggered when a message is sent',
  },
  {
    event_type: 'conversation.ended',
    description: 'Triggered when a conversation is ended',
  },
  {
    event_type: 'conversation.label.added',
    description: 'Triggered when a label is added to a conversation',
  },
  {
    event_type: 'conversation.label.deleted',
    description: 'Triggered when a label is removed from a conversation',
  },
  {
    event_type: 'call.new',
    description: 'Triggered when a call starts',
  },
  {
    event_type: 'call.ended',
    description: 'Triggered when a call ends',
  },
  {
    event_type: 'call.updated',
    description: 'Triggered when a call summary is generated',
  }
];
```

## **Test Your Webhook and Know What Will Be Sent**

Simulate different types of events to validate your webhook endpoint. This
section walks you through:

- How test requests are constructed
- What payload structure to expect

#### Endpoint

`POST https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/test`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Name        | Type   | Required | Description                                             |
| ----------- | ------ | -------- | ------------------------------------------------------- |
| event_type  | string | Yes      | The type of event to simulate (e.g. `conversation.new`) |
| webhook_url | string | Yes      | The URL to which the test payload will be sent          |

**Sample Request**

```bash
curl -X POST "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/test" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "conversation.new",
    "webhook_url": "https://api.example.com/test-webhook"
  }'
```

**Sample Successful Response**

The actual response body sent to your webhook_url depends on the `event_type`
provided. Below is an example response for the `conversation.new` event type:

```bash
{
  "id": "6e74c661-4c66-4d1e-81b0-64b2f4dcac98",
  "affect": "add",
  "version": "0.0.1",
  "timestamp": "2025-06-20T23:44:30.000000",
  "event_type": "conversation.new",
  "workspace": {
    "id": "workspace-123",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Example Conversation",
    "channel": "WEBCHAT",
    "customer": {
      "id": "cust-001",
      "name": "Test User",
      "email": "Test@example.com",
      "phone": "+123456789",
      "address": "Test AI Agent",
      "channel": "WEBCHAT"
    },
    "latest_inbound_message": {
      "id": "msg-in-123456",
      "direction": "INBOUND",
      "text": "Hello, I need help!",
      "type": "text",
      "created_at": "2025-06-20T23:44:00.000000"
    },
    "latest_outbound_message": {
      "id": "msg-out-123456",
      "direction": "OUTBOUND",
      "text": "Sure, how can I assist?",
      "type": "text",
      "created_at": "2025-06-20T23:44:30.000000"
    }
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user"
}


```

## **View Delivery Logs**

Learn how to retrieve delivery logs for your webhooks and what you can expect in
logs.

### Get Webhook Delivery Logs for a Workspace

Retrieves webhook delivery logs for a specific workspace. You can optionally
filter results by event type, delivery status, date range, and more.

#### Endpoint

`GET https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Query Parameter

The following optional query parameters are supported.

| Name              | Type     | Description                                                                                                                                                           |
| ----------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event_type`      | string   | Filter logs by event type (e.g. `conversation.new`)                                                                                                                   |
| `delivery_status` | string   | Filter by delivery status (`success`, `failed`)                                                                                                                       |
| `start_date`      | datetime | Return logs created on or after this date (ISO 8601 format). Example: `2024-06-01T23:59:59-07:00` (America/Los_Angeles), `2024-06-01T23:59:59+08:00` (Asia/Singapore) |
| `end_date`        | datetime | Return logs created on or before this date. Example: `2024-06-01T23:59:59-07:00` (America/Los_Angeles), `2024-06-01T23:59:59+08:00` (Asia/Singapore)                  |
| `order_by`        | string   | Sort results (default: `created_at:desc`). Format: `field:direction`                                                                                                  |
| `limit`           | integer  | Maximum number of results (default: 0 for unlimited)                                                                                                                  |
| `offset`          | integer  | Number of results to skip (default: 0)                                                                                                                                |

_Order By Options_

The `order_by` query parameter allows you to sort the delivery logs by a
specific field and direction.  
The format is `field:direction`, where direction can be either `asc` for
ascending or `desc` for descending.

**Supported fields for Order By:**

| `order_by` Value       | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `created_at:asc`       | Oldest logs first                               |
| `created_at:desc`      | Newest logs first (default)                     |
| `event_type:asc`       | Event type A–Z                                  |
| `event_type:desc`      | Event type Z–A                                  |
| `delivery_status:asc`  | Status A–Z (e.g. failed before success)         |
| `delivery_status:desc` | Status Z–A                                      |
| `status_code:asc`      | Lower HTTP status codes first (e.g. 200 → 500)  |
| `status_code:desc`     | Higher HTTP status codes first (e.g. 500 → 200) |

If not specified, the default is `created_at:desc`.

**Sample Request**

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

**Sample Successful Response**

```bash
{
  "total": 1,
  "data": [
    {
      "id": "1234567890abcdef",
      "workspace_id": "ws_123456",
      "event_id": "evt_987654321",
      "subscription_id": "29efe26f-eb8a-4ee8-9abf-d8651a31283e",
      "event_type": "conversation.new",
      "webhook_url": "https://api.example.com/webhooks/incoming",
      "delivery_status": "success",
      "status_code": "200",
      "response_body": "{\"status\": \"received\", \"message\": \"Webhook processed successfully\"}",
      "delivered_event_obj": {
        "id": "1246965",
        "workspace_id": "1246965",
        "workspace_name": "seasalt.ai bot",
        "value": {
          "event_type": "conversation.new",
          "event_source": "portal",
          "event_triggered_by": "kelly@seasalt.ai",
          "payload": {
            "conversation": {
              "id": "conv_123",
              "title": "New Conversation"
            }
          },
          "occurred_at": "2025-06-20T23:44:30.000000",
          "sent_at": "2025-06-20T23:44:30.000000",
          "subscription_created_by": "kelly@seasalt.ai",
          "subscription_updated_by": "kelly@seasalt.ai"
        }
      },
      "created_at": "2024-03-11T04:18:13.558258"
    }
  ]
}

```

### **Get Webhook Delivery Logs for a Subscription**

Retrieve webhook delivery logs tied to a specific subscription. Supports
optional filtering by event type, delivery status, date range, ordering, and
pagination.

#### Endpoint

`GET https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

| Name              | Type     | Description                                                                                                                                                           |
| ----------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event_type`      | string   | Filter logs by event type (e.g. `conversation.new`)                                                                                                                   |
| `delivery_status` | string   | Filter by delivery status (`success`, `failed`)                                                                                                                       |
| `start_date`      | datetime | Return logs created on or after this date (ISO 8601 format). Example: `2024-06-01T23:59:59-07:00` (America/Los_Angeles), `2024-06-01T23:59:59+08:00` (Asia/Singapore) |
| `end_date`        | datetime | Return logs created on or before this date. Example: `2024-06-01T23:59:59-07:00` (America/Los_Angeles), `2024-06-01T23:59:59+08:00` (Asia/Singapore)                  |
| `order_by`        | string   | Sort results (default: `created_at:desc`). Format: `field:direction`                                                                                                  |
| `limit`           | integer  | Maximum number of results (default: 0 for unlimited)                                                                                                                  |
| `offset`          | integer  | Number of results to skip (default: 0)                                                                                                                                |

#### Order By Options

The `order_by` query parameter allows you to sort the delivery logs by a
specific field and direction.  
The format is `field:direction`, where direction can be either `asc` for
ascending or `desc` for descending.

**Supported fields for ordering:**

| `order_by` Value       | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `created_at:asc`       | Oldest logs first                               |
| `created_at:desc`      | Newest logs first (default)                     |
| `event_type:asc`       | Event type A–Z                                  |
| `event_type:desc`      | Event type Z–A                                  |
| `delivery_status:asc`  | Status A–Z (e.g. failed before success)         |
| `delivery_status:desc` | Status Z–A                                      |
| `status_code:asc`      | Lower HTTP status codes first (e.g. 200 → 500)  |
| `status_code:desc`     | Higher HTTP status codes first (e.g. 500 → 200) |

If not specified, the default is `created_at:desc`.

**Sample Request**

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/{subscription_id}?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

**Sample Request**

```bash
{
  "total": 1,
  "data": [
    {
      "id": "1234567890abcdef",
      "workspace_id": "ws_123456",
      "event_id": "evt_987654321",
      "subscription_id": "29efe26f-eb8a-4ee8-9abf-d8651a31283e",
      "event_type": "conversation.new",
      "webhook_url": "https://api.example.com/webhooks/incoming",
      "delivery_status": "success",
      "status_code": "200",
      "response_body": "{\"status\": \"received\", \"message\": \"Webhook processed successfully\"}",
      "delivered_event_obj": {
        "id": "1246965",
        "workspace_id": "1246965",
        "workspace_name": "seasalt.ai bot",
        "value": {
          "event_type": "conversation.new",
          "event_source": "portal",
          "event_triggered_by": "kelly@seasalt.ai",
          "payload": {
            "conversation": {
              "id": "conv_123",
              "title": "New Conversation"
            }
          },
          "occurred_at": "2025-06-20T23:44:30.000000",
          "sent_at": "2025-06-20T23:44:30.000000",
          "subscription_created_by": "kelly@seasalt.ai",
          "subscription_updated_by": "kelly@seasalt.ai"
        }
      },
      "created_at": "2024-03-11T04:18:13.558258"
    }
  ]
}

```

### **Export Webhook Delivery Logs to Email**

Export webhook delivery logs for a workspace within a specific date range and
receive a download link via email.

#### Endpoint

`POST https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/export`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Name         | Type     | Required | Description                                                                                                                                                                                 |
| ------------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `email`      | string   | ✅       | The email address to receive the download link.                                                                                                                                             |
| `start_date` | datetime |          | Start date of the logs to export (ISO 8601 format). Example: `2024-06-01T23:59:59-07:00` (America/Los_Angeles), `2024-06-01T23:59:59+08:00` (Asia/Singapore)                                |
| `end_date`   | datetime |          | End date of the logs to export (ISO 8601 format). Example: `2024-06-01T23:59:59-07:00` (America/Los_Angeles), `2024-06-01T23:59:59+08:00` (Asia/Singapore)                                  |
| `lang`       | string   |          | Either `en-US` or `zh-TW`. We currently support two languages in the email template: English and Traditional Chinese. If any other value is provided, the template will default to English. |

**Sample Request**

```bash
curl -X POST "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/export" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2024-03-01T00:00:00Z",
    "end_date": "2024-03-31T23:59:59Z",
    "lang": "en-US",
    "email": "test@email.com"
  }'
```

**Sample Successful Response**

```bash
{
  "job_id": "export_job_abc123",
  "message": "Log export job started. You will receive an email once the file is ready."
}

```

##### Result

You will receive an email containing a secure download link to the exported log
file once the export is complete.

##### Notes

This is an asynchronous export. Processing time varies depending on the data
volume.

### Event Payload Schema Reference

This section provides a detailed breakdown of the payload schema for each
supported event type in the Webhook Notification API. Each event includes
standard metadata (like id, timestamp, workspace) and a structured data object
specific to the event. Use these schema definitions to correctly parse, process,
and respond to webhook notifications in your application.

#### conversation.new

This event is triggered when a new conversation is initiated within the
Seasalt.ai platform. It typically includes details about the conversation,
customer, and the latest messages exchanged.

**Payload Fields**

| Field                                     | Type     | Description                                       |
| ----------------------------------------- | -------- | ------------------------------------------------- |
| `id`                                      | `string` | Unique identifier of the event                    |
| `event_type`                              | `string` | Always `"conversation.new"`                       |
| `affect`                                  | `string` | Type of change, usually `"add"`                   |
| `version`                                 | `string` | Event schema version, e.g. `"0.0.1"`              |
| `timestamp`                               | `string` | When the event occurred, in ISO 8601 format       |
| `workspace.id`                            | `string` | Workspace ID associated with the event            |
| `workspace.name`                          | `string` | Workspace name                                    |
| `source.id`                               | `string` | ID of the event source (e.g., AI agent ID)        |
| `source.type`                             | `string` | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.) |
| `source.identifier`                       | `string` | Identifier or name of the bot or integration      |
| `data.conversation_id`                    | `string` | ID of the new conversation                        |
| `data.conversation_title`                 | `string` | Title of the conversation                         |
| `data.channel`                            | `string` | Channel where the conversation started            |
| `data.customer.id`                        | `string` | Customer ID                                       |
| `data.customer.name`                      | `string` | Customer name                                     |
| `data.customer.email`                     | `string` | Customer email address                            |
| `data.customer.phone`                     | `string` | Customer phone number                             |
| `data.customer.address`                   | `string` | Address or source identifier                      |
| `data.customer.channel`                   | `string` | Customer’s channel (should match `data.channel`)  |
| `data.latest_inbound_message.id`          | `string` | ID of the latest inbound message                  |
| `data.latest_inbound_message.direction`   | `string` | Always `"INBOUND"`                                |
| `data.latest_inbound_message.text`        | `string` | Message content                                   |
| `data.latest_inbound_message.type`        | `string` | Type of message (e.g. `"text"`)                   |
| `data.latest_inbound_message.created_at`  | `string` | Timestamp of message creation (ISO 8601)          |
| `data.latest_outbound_message.id`         | `string` | ID of the latest outbound message                 |
| `data.latest_outbound_message.direction`  | `string` | Always `"OUTBOUND"`                               |
| `data.latest_outbound_message.text`       | `string` | Message content                                   |
| `data.latest_outbound_message.type`       | `string` | Type of message (e.g. `"text"`)                   |
| `data.latest_outbound_message.created_at` | `string` | Timestamp of message creation (ISO 8601)          |

**Sample Event Payload**

```bash
{
  "id": "6e74c661-4c66-4d1e-81b0-64b2f4dcac98",
  "event_type": "conversation.new",
  "affect": "add",
  "version": "0.0.1",
  "timestamp": "2025-06-20T23:45:00.000000",
  "workspace": {
    "id": "workspace-123",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Test Example Conversation",
    "channel": "WEBCHAT",
    "customer": {
      "id": "fb0b4af0-ad6a-48a3-ad3c-d10b237b432c",
      "name": "Test User",
      "email": "Test@example.com",
      "phone": "+123456789",
      "address": "Test AI Agent",
      "channel": "WEBCHAT"
    },
    "latest_inbound_message": {
      "id": "msg-in-123456",
      "direction": "INBOUND",
      "text": "Hello, I need help!",
      "type": "text",
      "created_at": "2025-06-20T23:44:00.000000"
    },
    "latest_outbound_message": {
      "id": "msg-out-123456",
      "direction": "OUTBOUND",
      "text": "Sure, how can I assist?",
      "type": "text",
      "created_at": "2025-06-20T23:44:30.000000"
    }
  }
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}

```

#### conversation.updated

This event is triggered when an existing conversation is updated—such as changes
to customer info, title, or other metadata.

**Payload Fields**

| Field                     | Type                | Description                                       |
| ------------------------- | ------------------- | ------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                    |
| `event_type`              | `string`            | Always `"conversation.updated"`                   |
| `affect`                  | `string`            | Type of change, typically `"change"`              |
| `version`                 | `string`            | Event schema version, e.g. `"0.0.1"`              |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format       |
| `workspace.id`            | `string`            | Workspace ID associated with the event            |
| `workspace.name`          | `string`            | Workspace name                                    |
| `source.id`               | `string`            | ID of the event source (e.g., AI agent ID)        |
| `source.type`             | `string`            | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.) |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration      |
| `data.conversation_id`    | `string`            | ID of the updated conversation                    |
| `data.conversation_title` | `string`            | Title of the conversation                         |
| `data.channel`            | `string`            | Channel where the conversation takes place        |
| `data.customer.id`        | `string`            | Customer ID                                       |
| `data.customer.name`      | `string`            | Customer name                                     |
| `data.customer.email`     | `string`            | Customer email address                            |
| `data.customer.phone`     | `string`            | Customer phone number                             |
| `data.customer.address`   | `string`            | Address or source identifier                      |
| `data.customer.channel`   | `string`            | Customer’s channel (should match `data.channel`)  |
| `data.updated_fields`     | `array of string`   | List of fields that were updated                  |
| `data.previous`           | `object`            | Previous values before the update                 |
| `data.current`            | `object`            | Current values after the update                   |
| `data.updated_by.id`      | `string` (optional) | ID of the user or agent who made the update       |
| `data.updated_by.name`    | `string` (optional) | Name of the user or agent who made the update     |
| `data.updated_by.type`    | `string` (optional) | Type of entity (e.g., `agent`, `system`)          |
| `data.updated_at`         | `string`            | Timestamp of the update (ISO 8601)                |

**Sample Event Payload**

```bash
{
  "id": "cb1537d3-712e-44cf-8709-11b3fe55177a",
  "event_type": "conversation.updated",
  "affect": "change",
  "version": "0.0.1",
  "timestamp": "2025-06-20T23:45:00.000000",
  "workspace": {
    "id": "workspace-123",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Test Example Conversation",
    "channel": "WEBCHAT",
    "customer": {
      "id": "fb0b4af0-ad6a-48a3-ad3c-d10b237b432c",
      "name": "Test User",
      "email": "zapier@example.com",
      "phone": "+123456789",
      "address": "Test AI Agent",
      "channel": "WEBCHAT"
    },
    "updated_fields": ["is_unread"],
    "previous": {
      "is_unread": "false"
    },
    "current": {
      "is_unread": "true"
    },
    "updated_by": {
      "id": "user_123",
      "name": "Admin",
      "type": "agent"
    },
    "updated_at": "2025-06-20T23:44:59.000000"
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}
```

#### conversation.ended

This event is triggered when a conversation ends or is closed. It shares the
same structure as conversation.updated, with the affect field set to "delete".

**Payload Fields**

| Field                     | Type                | Description                                                    |
| ------------------------- | ------------------- | -------------------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                                 |
| `event_type`              | `string`            | Always `"conversation.ended"`                                  |
| `affect`                  | `string`            | Always `"delete"`                                              |
| `version`                 | `string`            | Event schema version, e.g. `"0.0.1"`                           |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format                    |
| `workspace.id`            | `string`            | Workspace ID associated with the event                         |
| `workspace.name`          | `string`            | Workspace name                                                 |
| `source.id`               | `string`            | ID of the event source (e.g., AI agent ID)                     |
| `source.type`             | `string`            | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.)              |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration                   |
| `data.conversation_id`    | `string`            | ID of the ended conversation                                   |
| `data.conversation_title` | `string`            | Title of the conversation                                      |
| `data.channel`            | `string`            | Channel where the conversation took place                      |
| `data.customer.id`        | `string`            | Customer ID                                                    |
| `data.customer.name`      | `string`            | Customer name                                                  |
| `data.customer.email`     | `string`            | Customer email address                                         |
| `data.customer.phone`     | `string`            | Customer phone number                                          |
| `data.customer.address`   | `string`            | Address or source identifier                                   |
| `data.customer.channel`   | `string`            | Customer’s channel (should match `data.channel`)               |
| `data.updated_fields`     | `array of string`   | List of fields that were changed before the conversation ended |
| `data.previous`           | `object`            | Previous values before the final update                        |
| `data.current`            | `object`            | Final values at the moment the conversation ended              |
| `data.updated_by.id`      | `string` (optional) | ID of the user or agent who ended the conversation             |
| `data.updated_by.name`    | `string` (optional) | Name of the user or agent                                      |
| `data.updated_by.type`    | `string` (optional) | Type of entity (e.g., `agent`, `system`)                       |
| `data.updated_at`         | `string`            | Timestamp when the conversation was ended                      |

**Sample Event Payload**

```bash
{
  "id": "cb1537d3-712e-44cf-8709-11b3fe55177a",
  "event_type": "conversation.ended",
  "affect": "delete",
  "version": "0.0.1",
  "timestamp": "2025-06-20T23:45:00.000000",
  "workspace": {
    "id": "workspace-123",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Test Example Conversation",
    "channel": "WEBCHAT",
    "customer": {
      "id": "fb0b4af0-ad6a-48a3-ad3c-d10b237b432c",
      "name": "Test User",
      "email": "Test@example.com",
      "phone": "+123456789",
      "address": "Test AI Agent",
      "channel": "WEBCHAT"
    },
    "updated_fields": ["CSAT_SUBMISSION"],
    "previous": "null",
    "current": {"rating": 5, "comment": "Quick and accurate response. Nice experience!"},
    "updated_by": {"type": "USER", "id": "user-abc-123", "name": "Test User"},
    "updated_at": "2025-06-20T23:44:59.000000"
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}
```

#### message.new

This event is triggered whenever a new message is sent in a conversation. It
includes detailed metadata about the message content, sender, and direction.

**Payload Fields**

| Field                     | Type                | Description                                                   |
| ------------------------- | ------------------- | ------------------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                                |
| `event_type`              | `string`            | Always `"message.new"`                                        |
| `affect`                  | `string`            | Always `"add"`                                                |
| `version`                 | `string`            | Event schema version, e.g. `"0.0.1"`                          |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format                   |
| `workspace.id`            | `string`            | Workspace ID associated with the event                        |
| `workspace.name`          | `string`            | Workspace name                                                |
| `source.id`               | `string`            | ID of the event source (e.g., AI agent ID)                    |
| `source.type`             | `string`            | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.)             |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration                  |
| `data.conversation_id`    | `string`            | ID of the conversation the message belongs to                 |
| `data.conversation_title` | `string`            | Title of the conversation                                     |
| `data.message_id`         | `string`            | Unique identifier of the message                              |
| `data.direction`          | `string`            | Message direction (`INBOUND` or `OUTBOUND`)                   |
| `data.created_at`         | `string`            | When the message was created (ISO 8601 format)                |
| `data.sender.type`        | `string`            | Sender type (`CUSTOMER`, `BOT`, `AGENT`, etc.)                |
| `data.sender.id`          | `string`            | ID of the sender                                              |
| `data.sender.name`        | `string` (optional) | Name of the sender                                            |
| `data.content.type`       | `string`            | Type of content (`text`, `image`, etc.)                       |
| `data.content.text`       | `string`            | Textual content of the message                                |
| `data.content.data`       | `object` (optional) | Additional data for rich content (e.g., image URLs, metadata) |

**Sample Event Payload**

```bash
{
  "id": "3a3b8bc0-dc3d-43b4-a957-17c2fe1ad153",
  "event_type": "message.new",
  "affect": "add",
  "version": "0.0.1",
  "timestamp": "2025-06-20T23:46:00.000000",
  "workspace": {
    "id": "workspace-123",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Test Example Conversation",
    "message_id": "msg-789",
    "direction": "INBOUND",
    "created_at": "2025-06-20T23:45:59.000000",
    "sender": {
      "type": "CUSTOMER",
      "id": "fb0b4af0-ad6a-48a3-ad3c-d10b237b432c",
      "name": "Test User"
    },
    "content": {
      "type": "text",
      "text": "Hello, I need help!",
      "data": null
    }
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}
```

#### conversation.label.added

This event is triggered when one or more labels are attached to a conversation.
It includes details about the updated fields, customer info, who added the
label, and when.

**Payload Fields**

| Field                     | Type                | Description                                         |
| ------------------------- | ------------------- | --------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                      |
| `event_type`              | `string`            | Always `"conversation.label.added"`                 |
| `affect`                  | `string`            | Always `"add"`                                      |
| `version`                 | `string`            | Event schema version, e.g., `"0.0.1"`               |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format         |
| `workspace.id`            | `string`            | Workspace ID associated with the event              |
| `workspace.name`          | `string`            | Workspace name                                      |
| `source.id`               | `string`            | ID of the event source                              |
| `source.type`             | `string`            | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.)   |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration        |
| `data.conversation_id`    | `string`            | ID of the conversation                              |
| `data.conversation_title` | `string`            | Title of the conversation                           |
| `data.channel`            | `string`            | Channel type of the conversation                    |
| `data.customer`           | `object`            | Customer information (id, name, contact info, etc.) |
| `data.updated_fields`     | `array of string`   | List of updated fields (likely includes `labels`)   |
| `data.previous`           | `object` (optional) | Previous values of updated fields                   |
| `data.current`            | `object` (optional) | Current values of updated fields                    |
| `data.added_by`           | `object` (optional) | The user or bot who added the label                 |
| `data.added_at`           | `string`            | Timestamp when the label was added                  |
| `data.labels`             | `array of object`   | List of label objects (e.g., label id and name)     |

**Sample Event Payload**

```bash
{
  "id": "ba01d246-3a8c-4e63-a191-28215797388b",
  "event_type": "conversation.label.added",
  "affect": "add",
  "version": "0.0.1",
  "timestamp": "2025-06-20T23:50:00.000000",
  "workspace": {
    "id": "workspace-123",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Test Example Conversation",
    "channel": "WEBCHAT",
    "customer": {
      "id": "fb0b4af0-ad6a-48a3-ad3c-d10b237b432c",
      "name": "Test User",
      "email": "Test@example.com",
      "phone": "+123456789",
      "address": "Test AI Agent",
      "channel": "WEBCHAT"
    },
    "updated_fields": ["labels"],
    "previous": {},
    "current": {
      "labels": [
        {
          "id": "90c51757408941e2834f76392249b10f",
          "color": "#a7927f",
          "label": "solved",
          "created_at": "2025-05-10T00:20:38.834259",
          "updated_at": "2025-05-10T00:20:38.834259",
          "description": "",
          "workspace_id": Zapier.get_base_sample_data()[0],
        },
      ]
    },
    "added_by": {
      "id": "user-001",
      "type": "agent",
      "name": "Support Agent"
    },
    "added_at": "2025-06-20T23:50:00.000000",
    "labels": [
     {
        "id": "90c51757408941e2834f76392249b10f",
        "name": "solved",
        "type": "CONVERSATION",
        "color": "#a7927f",
        "is_system": False,
        "description": "",
      }
    ]
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}

```

#### conversation.label.deleted

This event is triggered when one or more labels are removed from a conversation.
It includes details about which fields changed, who removed the label, and when.

**Payload Fields**

| Field                     | Type                | Description                                         |
| ------------------------- | ------------------- | --------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                      |
| `event_type`              | `string`            | Always `"conversation.label.deleted"`               |
| `affect`                  | `string`            | Always `"delete"`                                   |
| `version`                 | `string`            | Event schema version, e.g., `"0.0.1"`               |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format         |
| `workspace.id`            | `string`            | Workspace ID associated with the event              |
| `workspace.name`          | `string`            | Workspace name                                      |
| `source.id`               | `string`            | ID of the event source                              |
| `source.type`             | `string`            | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.)   |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration        |
| `data.conversation_id`    | `string`            | ID of the conversation                              |
| `data.conversation_title` | `string`            | Title of the conversation                           |
| `data.channel`            | `string`            | Channel type of the conversation                    |
| `data.customer`           | `object`            | Customer information (id, name, contact info, etc.) |
| `data.updated_fields`     | `array of string`   | List of updated fields (likely includes `labels`)   |
| `data.previous`           | `object` (optional) | Previous values of updated fields                   |
| `data.current`            | `object` (optional) | Current values of updated fields                    |
| `data.removed_by`         | `object` (optional) | The user or bot who removed the label               |
| `data.removed_at`         | `string`            | Timestamp when the label was removed                |
| `data.labels`             | `array of object`   | List of label objects that were removed             |

**Sample Event Payload**

```bash
{
  "id": "ab1f7a9b-3a7e-4894-9b35-ef3eaa0e2174",
  "event_type": "conversation.label.deleted",
  "affect": "delete",
  "version": "0.0.1",
  "timestamp": "2025-06-21T00:00:00.000000",
  "workspace": {
    "id": "workspace-123",
    "name": "Zapier Workspace"
  },
  "source": {
    "id": "source-456",
    "type": "WEBCHAT",
    "identifier": "Test AI Agent"
  },
  "data": {
    "conversation_id": "conv-789",
    "conversation_title": "Test Example Conversation",
    "channel": "WEBCHAT",
    "customer": {
      "id": "fb0b4af0-ad6a-48a3-ad3c-d10b237b432c",
      "name": "Test User",
      "email": "Test@example.com",
      "phone": "+123456789",
      "address": "Test AI Agent",
      "channel": "WEBCHAT"
    },
    "updated_fields": ["labels"],
    "previous": {
      "labels": [
        {
          "id": "8d99e9b041f04447858cde7506cee4d5",
          "color": "#565e9c",
          "label": "newUser",
          "created_at": "2025-04-08T02:48:25.059243",
          "updated_at": "2025-04-08T02:48:25.059243",
          "description": "this is a new user",
          "workspace_id": Zapier.get_base_sample_data()[0],
        },
        {
            "id": "90c51757408941e2834f76392249b10f",
            "color": "#a7927f",
            "label": "solved",
            "created_at": "2025-05-10T00:20:38.834259",
            "updated_at": "2025-05-10T00:20:38.834259",
            "description": "",
            "workspace_id": Zapier.get_base_sample_data()[0],
        },
      ]
    },
    "current": {
      [
        {
          "id": "8d99e9b041f04447858cde7506cee4d5",
          "color": "#565e9c",
          "label": "newUser",
          "created_at": "2025-04-08T02:48:25.059243",
          "updated_at": "2025-04-08T02:48:25.059243",
          "description": "this is a new user",
          "workspace_id": Zapier.get_base_sample_data()[0],
      }
    ]},
    "removed_by": {
      "id": "user-002",
      "type": "agent",
      "name": "Support Agent"
    },
    "removed_at": "2025-06-21T00:00:00.000000",
    "labels": [
      {
          "id": "90c51757408941e2834f76392249b10f",
          "name": "solved",
          "type": "CONVERSATION",
          "color": "#a7927f",
          "is_system": False,
          "description": "",
      }
    ],
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}
```

#### call.new

This event is triggered when a new call is initiated. It includes information
about the caller, callee, call direction, channel, and metadata.

**Payload Fields**

| Field                     | Type                | Description                                             |
| ------------------------- | ------------------- | ------------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                          |
| `event_type`              | `string`            | Always `"call.new"`                                     |
| `affect`                  | `string`            | Always `"add"`                                          |
| `version`                 | `string`            | Event schema version, e.g., `"0.0.1"`                   |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format             |
| `workspace.id`            | `string`            | Workspace ID associated with the event                  |
| `workspace.name`          | `string`            | Workspace name                                          |
| `source.id`               | `string`            | ID of the event source                                  |
| `source.type`             | `string`            | Channel type (e.g., `WEBCHAT`, `MESSENGER`, etc.)       |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration            |
| `data.conversation_id`    | `string`            | ID of the associated conversation                       |
| `data.conversation_title` | `string`            | Title of the conversation                               |
| `data.channel`            | `string`            | Channel where the call took place                       |
| `data.direction`          | `string`            | `INBOUND` or `OUTBOUND`                                 |
| `data.call_from`          | `object`            | Entity initiating the call (type, id, name, address)    |
| `data.call_to`            | `object`            | Entity receiving the call (type, id, name, address)     |
| `data.started_at`         | `string`            | Timestamp when the call started (ISO 8601 format)       |
| `data.metadata`           | `object` (optional) | Additional metadata, such as SIP info or system details |

**Sample Event Payload**

```bash
{
  "id": "e1b57c9f-dcd9-4bc1-bdc8-cfc9960c011e",
  "event_type": "call.new",
  "affect": "add",
  "version": "0.0.1",
  "timestamp": "2025-06-21T09:00:00.000000",
  "workspace": {
    "id": "workspace-456",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-999",
    "type": "SEAX_CALL",
    "identifier": "Test Callbot"
  },
  "data": {
    "conversation_id": "conv-call-001",
    "conversation_title": "+11234567890",
    "channel": "SEAX_CALL",
    "direction": "INBOUND",
    "started_at": "2025-06-21T09:00:00.000000",
    "call_from": {
      "id": "cust-001",
      "id": "+123456789",
      "name": "Zapier AI Agent",
      "type": "AGENT",
      "address": "+123456789",
      "conversation_id": "123",
      "conversation_title": "+123456789",
    },
    "call_to": {
      "id": "agent-001",
      "name": "+123456789",
      "type": "CUSTOMER",
      "address": "+123456789",
      "conversation_id": "123",
      "conversation_title": "+123456789",
    },
    "started_at": "2025-06-21T09:00:00.000000",
    "metadata": {
      "sip_session_id": "abc123",
      "recording_enabled": true
    }
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}

```

#### call.ended

This event is triggered when a call ends. It contains the call participants,
duration, reason for ending, and optional recording information.

**Payload Fields**

| Field                      | Type                | Description                                                      |
| -------------------------- | ------------------- | ---------------------------------------------------------------- |
| `id`                       | `string`            | Unique identifier of the event                                   |
| `event_type`               | `string`            | Always `"call.ended"`                                            |
| `affect`                   | `string`            | Always `"delete"`                                                |
| `version`                  | `string`            | Event schema version, e.g., `"0.0.1"`                            |
| `timestamp`                | `string`            | When the event occurred, in ISO 8601 format                      |
| `workspace.id`             | `string`            | Workspace ID associated with the event                           |
| `workspace.name`           | `string`            | Workspace name                                                   |
| `source.id`                | `string`            | ID of the event source                                           |
| `source.type`              | `string`            | Channel type (e.g., `SEAX_CALL`, `WHATSAPP`)                     |
| `source.identifier`        | `string`            | Identifier or name of the bot or integration                     |
| `data.conversation_id`     | `string`            | ID of the associated conversation                                |
| `data.conversation_title`  | `string`            | Title of the conversation                                        |
| `data.channel`             | `string`            | Channel where the call took place                                |
| `data.direction`           | `string`            | `INBOUND` or `OUTBOUND`                                          |
| `data.duration_seconds`    | `integer`           | Duration of the call in seconds                                  |
| `data.finish_reason`       | `string`            | Reason the call ended (e.g., `completed`, `abandoned`, `failed`) |
| `data.call_from`           | `object`            | Caller info (type, id, name, address)                            |
| `data.call_to`             | `object`            | Callee info (type, id, name, address)                            |
| `data.finished_at`         | `string`            | When the call ended (ISO 8601)                                   |
| `data.finished_by`         | `string`            | Who ended the call (timestamp)                                   |
| `data.recording_available` | `boolean`           | Whether a recording is available                                 |
| `data.recording_url`       | `string` (optional) | URL to download the call recording                               |

**Sample Event Payload**

```bash
{
  "id": "2c72e50e-68ae-4a97-8f20-cdffedexample",
  "event_type": "call.ended",
  "affect": "delete",
  "version": "0.0.1",
  "timestamp": "2025-06-21T09:15:00.000000",
  "workspace": {
    "id": "workspace-456",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-999",
    "type": "SEAX_CALL",
    "identifier": "Test Callbot"
  },
  "data": {
    "conversation_id": "conv-call-001",
    "conversation_title": "+11234567890",
    "channel": "SEAX_CALL",
    "direction": "INBOUND",
    "duration_seconds": 300,
    "finish_reason": "completed",
    "call_from": {
      "id": "cust-001",
      "id": "+123456789",
      "name": "Zapier AI Agent",
      "type": "AGENT",
      "address": "+123456789",
      "conversation_id": "123",
      "conversation_title": "+123456789",
    },
    "call_to": {
      "id": "agent-001",
      "name": "+123456789",
      "type": "CUSTOMER",
      "address": "+123456789",
      "conversation_id": "123",
      "conversation_title": "+123456789",
    },
    "finished_at": "2025-06-21T09:15:00.000000",
    "finished_by": "2025-06-21T09:15:00.000000",
    "recording_available": true,
    "recording_url": "https://recordings.example.com/recording1234.mp3"
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}
```

#### call.updated

This event is triggered when details of an ongoing or completed call are
updated. It is typically used to reflect changes such as transcription
availability, additional metadata, or corrections.

**Payload Fields**

| Field                     | Type                | Description                                                 |
| ------------------------- | ------------------- | ----------------------------------------------------------- |
| `id`                      | `string`            | Unique identifier of the event                              |
| `event_type`              | `string`            | Always `"call.updated"`                                     |
| `affect`                  | `string`            | Always `"update"`                                           |
| `version`                 | `string`            | Event schema version, e.g., `"0.0.1"`                       |
| `timestamp`               | `string`            | When the event occurred, in ISO 8601 format                 |
| `workspace.id`            | `string`            | Workspace ID associated with the event                      |
| `workspace.name`          | `string`            | Workspace name                                              |
| `source.id`               | `string`            | ID of the event source                                      |
| `source.type`             | `string`            | Channel type (e.g., `SEAX_CALL`, `WHATSAPP`)                |
| `source.identifier`       | `string`            | Identifier or name of the bot or integration                |
| `data.conversation_id`    | `string`            | ID of the associated conversation                           |
| `data.conversation_title` | `string`            | Title of the conversation                                   |
| `data.call_id`            | `string` (optional) | ID of the call being updated                                |
| `data.update_reason`      | `string` (optional) | Description of why the call was updated                     |
| `data.previous`           | `object` (optional) | Previous values of updated fields                           |
| `data.current`            | `object` (optional) | New/current values of updated fields                        |
| `data.updated_at`         | `string`            | When the update occurred (ISO 8601 format)                  |
| `data.resources`          | `object` (optional) | Additional attached data, such as transcription or analysis |

**Sample Event Payload**

```bash
{
  "id": "fcfe4bfa-8e04-4710-a10a-9f20c5e83ee3",
  "event_type": "call.updated",
  "affect": "update",
  "version": "0.0.1",
  "timestamp": "2025-06-22T10:10:00.000000",
  "workspace": {
    "id": "workspace-456",
    "name": "Test Workspace"
  },
  "source": {
    "id": "source-999",
    "type": "SEAX_CALL",
    "identifier": "Test Callbot"
  },
  "data": {
    "conversation_id": "conv-call-001",
    "conversation_title": "+11234567890",
    "call_id": "call-abc-123",
    "update_reason": "Transcription completed",
    "previous": {
      "recording_url": null
    },
    "update_reason": "recording_ready",
    "current": {
      "recording_url": "https://recordings.example.com/recording1234.mp3"
    },
    "updated_at": "2025-06-22T10:10:00.000000",
    "resources": {
      "session_id": "789456123",
      "channel_type": "SEAX_CALL",
      "conversation_id": "123456",
}
  },
  "subscription_created_by": "Test_user",
  "subscription_updated_by": "Test_user",
}
```
