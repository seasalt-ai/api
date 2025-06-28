---
title: Event Webhooks 
linkTitle: Event Webhooks API Tutorial
type: docs
weight: 1
---

## Overview

A webhook-based notification system that lets your services receive
real-time updates from Seasalt products like SeaChat. Whether you want to track
new conversations, missed calls, or contact changes, using the following endpoints ensures you stay
informed the moment it happens. With support for multiple event types and
delivery modes (immediate, delayed, batched), Portal's Event Webhooks are ideal for diverse
automation and integration needs. This section introduces the Event Webhooks API, a
webhook-based notification system that allows your application to receive
real-time updates when specific events occur within the Seasalt platform. You'll
learn how Event Webhooks fits into the broader Seasalt architecture and what problems
it solves.

You can also access the RESTful API docs of Event Webhooks [here](./Docs/notify-api/)

---

## Prerequisites

**Prepare Your Webhook Receiver**

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

`POST https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/subscription`

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
[this endpoint](#get-all-supported-event-types).

- `conversation.new`
- `conversation.updated`
- `message.new`
- `conversation.label.added`
- `conversation.label.deleted`
- `conversation.ended`
- `call.new`
- `call.updated`
- `call.ended`
- `call.missed`
- `contact.new`
- `contact.updated`
- `contact.deleted`
- `contact.label.added`
- `contact.label.deleted`

#### Sample Request

```javascript
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

#### Sample Successful Response

```javascript
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

`GET https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

You must provide your API key in the `X-API-KEY` header.

#### Sample Request

```javascript
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>"
```

#### Sample Successful Response

```javascript
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

`GET https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/subscription`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Query Parameter

We support the following optional queries to retrieve subscriptions. If
not provided, all subscriptions for the workspace will be returned.

| Name       | Type   | Required | Default           | Description                                                   |
| ---------- | ------ | -------- | ----------------- | ------------------------------------------------------------- |
| `order_by` | string |          | `created_at:desc` | Order items by field and direction. Format: `field:direction` |
| `type`     | string |          |                   | Filter by subscription type. Enum: `SEASALT`, `ZAPIER`        |

##### Sample Request

```javascript
curl -X GET
https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription
-H 'X-API-KEY: <your_api_key>'

```

##### Sample Successful Response

```javascript
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

`PATCH https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

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

#### Sample Request

```javascript
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

##### Sample Successful Response

```javascript
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

`DELETE https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Sample Request

```javascript
curl -X DELETE "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>"
```

##### Sample Successful Response

HTTP Status Code: 204 No Content

## **Get a List of Supported Events**

Retrieve a list of all event types that can be used when creating or updating
webhook subscriptions. Each event type includes a brief description of when it
is triggered.

#### Endpoint

`GET https://portal.seasalt.ai/notify-api/api/v1/event_types`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Sample Request

```javascript
curl -X GET "https://portal.seasalt.ai/notify/api/v1/event_types" \
  -H "X-API-KEY: <your_api_key>"
```

##### Sample Successful Response

```javascript
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
  },
  {
    event_type: 'call.missed',
    description: 'Triggered when a call is missed',
  },
  {
    event_type: 'contact.new',
    description: 'Triggered when a contact is created',
  },
  {
    event_type: 'contact.updated',
    description: 'Triggered when a contact is updated',
  },
  {
    event_type: 'contact.deleted',
    description: 'Triggered when a contact is deleted',
  },
  {
    event_type: 'contact.label.added',
    description: 'Triggered when a label is added to a contact',
  },
  {
    event_type: 'contact.label.deleted',
    description: 'Triggered when a label is removed from a contact',
  },
];
```

## **Test Your Webhook and Know What Will Be Sent**

Simulate different types of events to validate your webhook endpoint. This
section walks you through:

- How test requests are constructed
- What payload structure to expect

#### Endpoint

`POST https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/test`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Name        | Type   | Required | Description                                             |
| ----------- | ------ | -------- | ------------------------------------------------------- |
| event_type  | string | Yes      | The type of event to simulate (e.g. `conversation.new`) |
| webhook_url | string | Yes      | The URL to which the test payload will be sent          |

#### Sample Request

```javascript
curl -X POST "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/test" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "conversation.new",
    "webhook_url": "https://api.example.com/test-webhook"
  }'
```

##### Sample Successful Response

The actual response body sent to your webhook_url depends on the `event_type`
provided. Below is an example response for the `conversation.new` event type:

```javascript
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

`GET https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/logs`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Query Parameter

The following optional query parameters are supported.

| Name              | Type     | Description                                                          |
| ----------------- | -------- | -------------------------------------------------------------------- |
| `event_type`      | string   | Filter logs by event type (e.g. `conversation.new`)                  |
| `delivery_status` | string   | Filter by delivery status (`success`, `failed`)                      |
| `start_date`      | datetime | Return logs created on or after this date (ISO 8601 format)          |
| `end_date`        | datetime | Return logs created on or before this date                           |
| `order_by`        | string   | Sort results (default: `created_at:desc`). Format: `field:direction` |
| `limit`           | integer  | Maximum number of results (default: 0 for unlimited)                 |
| `offset`          | integer  | Number of results to skip (default: 0)                               |

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

#### Sample Request

```javascript
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

##### Sample Successful Response

```javascript
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
        "id": 1246965,
        "workspace_id": 1246965,
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
          "occurred_at": 1462216307945,
          "sent_at": 1462216307945,
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

`GET https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/logs/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

| Name              | Type     | Description                                                          |
| ----------------- | -------- | -------------------------------------------------------------------- |
| `event_type`      | string   | Filter logs by event type (e.g. `conversation.new`)                  |
| `delivery_status` | string   | Filter by delivery status (`success`, `failed`)                      |
| `start_date`      | datetime | Return logs created on or after this date (ISO 8601 format)          |
| `end_date`        | datetime | Return logs created on or before this date                           |
| `order_by`        | string   | Sort results (default: `created_at:desc`). Format: `field:direction` |
| `limit`           | integer  | Maximum number of results (default: 0 for unlimited)                 |
| `offset`          | integer  | Number of results to skip (default: 0)                               |

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

#### Sample Request

```javascript
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/{subscription_id}?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

##### Sample Successful Response

```javascript
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
        "id": 1246965,
        "workspace_id": 1246965,
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
          "occurred_at": 1462216307945,
          "sent_at": 1462216307945,
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

`POST https://portal.seasalt.ai/notify-api/api/v1/workspaces/{workspace_id}/logs/export`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Name         | Type     | Required | Description                                         |
| ------------ | -------- | -------- | --------------------------------------------------- |
| `email`      | string   | ✅       | The email address to receive the download link.     |
| `start_date` | datetime |          | Start date of the logs to export (ISO 8601 format). |
| `end_date`   | datetime |          | End date of the logs to export (ISO 8601 format).   |
| `lang`       | string   |          | Language/locale code (e.g., `en-US`, `zh-TW`).      |

Supported lang Values You may specify any valid
[ISO 639-1](https://www.iso.org/iso-639-language-code) or regional code, such
as: en-US, zh-TW, zh-CN, ja-JP, fr-FR, de-DE, es, vi-VN, etc.

##### Sample Request

```javascript
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

##### Sample Successful Response

```javascript
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
