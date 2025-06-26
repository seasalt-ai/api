---
title: Webhook
linkTitle: Webhook API
type: docs
weight: 1
---

## Overview

SeaNotify is a webhook-based notification system that lets your services receive
real-time updates from Seasalt products like SeaChat. Whether you want to track
new conversations, missed calls, or contact changes, SeaNotify ensures you stay
informed the moment it happens. With support for multiple event types and
delivery modes (immediate, delayed, batched), SeaNotify is ideal for diverse
automation and integration need This section introduces the SeaNotify API, a
webhook-based notification system that allows your application to receive
real-time updates when specific events occur within the Seasalt platform. You'll
learn how SeaNotify fits into the broader Seasalt architecture and what problems
it solves.

You can also access the RESTful API docs of SeaNotify here:  
[https://portal.seasalt.ai/notify/redoc](https://portal.seasalt.ai/notify/redoc)

---

## Prerequisites

Before you can interact with the SeaNotify API, ensure the following are in
place:

### **1\. A Seasuite Portal Account**

Sign up or log into your [Seasuite Portal](https://portal.seasalt.ai/).

### **2\. Generate Your API Key**

All APIs require a valid API key issued from your workspace.

- Go to **Settings → API Key** tab.

- Click **Add New Key**.

- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

### **3\. Prepare Your Webhook Receiver**

Your server must:

- Be publicly accessible over **HTTPS**

- Accept **POST** requests

- Handle **application/json** payloads

---

## Subscription APIs

This section explains how to manage webhook subscriptions in your workspace.

### Create a Subscription

Create a new webhook subscription in your SeaNotify workspace.

#### Endpoint

`POST /api/v1/workspaces/{workspace_id}/subscription`

Use this endpoint to register a webhook that will receive event notifications
from SeaNotify.

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

#### Supported Event Types

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

#### Successful Response

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

### Retrieve a Subscription

This endpoint retrieves the details of a specific webhook subscription by its
ID.

#### Endpoint

`GET /api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

You must provide your API key in the `X-API-KEY` header.

#### Sample Request

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>"
```

#### Successful Response

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

`GET /api/v1/workspaces/{workspace_id}/subscription`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Query Parameter

We supports the following optional queries so you can retrieve subscriptions. If
not provided, we will return the all the subscriptions for the workspace.

| Name       | Type   | Required | Default           | Description                                                   |
| ---------- | ------ | -------- | ----------------- | ------------------------------------------------------------- |
| `order_by` | string |          | `created_at:desc` | Order items by field and direction. Format: `field:direction` |
| `type`     | string |          |                   | Filter by subscription type. Enum: `SEASALT`, `ZAPIER`        |

##### Sample Request

```bash
curl -X GET
https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription
-H 'X-API-KEY: <your_api_key>'

```

##### Successful Response

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

### Update a Subscription

Modify an existing webhook subscription to update its webhook URL, event types,
status, or type.

#### Endpoint

`PATCH /api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body / Query Parameter

| Field       | Type     | Required | Description                                        |
| ----------- | -------- | -------- | -------------------------------------------------- |
| webhook_url | string   | No       | The URL to which webhook events will be delivered. |
| event_types | string[] | No       | A list of event types you want to subscribe to.    |
| is_enabled  | boolean  | No       | Whether the subscription is active.                |
| type        | string   | No       | Type of subscription. Enum: `SEASALT`, `ZAPIER`.   |
| updated_by  | string   | Yes      | Email or identifier of the user making the update. |

#### Sample Request

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

##### Successful Response

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

### Remove a Subscription

Delete an existing webhook subscription from your workspace. This action
permanently disables event delivery to the specified webhook URL.

#### Endpoint

`DELETE /api/v1/workspaces/{workspace_id}/subscription/{subscription_id}`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body / Query Parameter

No request body is required.

#### Sample Request

```bash
curl -X DELETE "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/subscription/{subscription_id}" \
  -H "X-API-KEY: <your_api_key>"
```

##### Successful Response

HTTP Status Code: 204 No Content

## Get a List of Supported Events

Lists and explains all available event types supported. This helps you
understand which events your webhook can listen to

### Get All Supported Event Types

Retrieve a list of all event types that can be used when creating or updating
webhook subscriptions. Each event type includes a brief description of when it
is triggered.

#### Endpoint

`GET /api/v1/event_types`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body / Query Parameter

No request body or query parameters are required.

#### Sample Request

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/event_types" \
  -H "X-API-KEY: <your_api_key>"
```

##### Successful Response

```bash
[
  {
    "event_type": "conversation.new",
    "description": "Triggered when a new conversation is created"
  },
  {
    "event_type": "conversation.updated",
    "description": "Triggered when a conversation is updated"
  },
  {
    "event_type": "message.new",
    "description": "Triggered when a message is sent"
  },
  {
    "event_type": "conversation.ended",
    "description": "Triggered when a conversation is ended"
  },
  {
    "event_type": "conversation.label.added",
    "description": "Triggered when a label is added to a conversation"
  },
  {
    "event_type": "conversation.label.deleted",
    "description": "Triggered when a label is removed from a conversation"
  },
  {
    "event_type": "call.new",
    "description": "Triggered when a call starts"
  },
  {
    "event_type": "call.ended",
    "description": "Triggered when a call ends"
  },
  {
    "event_type": "call.updated",
    "description": "Triggered when a call summary is generated"
  },
  {
    "event_type": "call.missed",
    "description": "Triggered when a call is missed"
  },
  {
    "event_type": "contact.new",
    "description": "Triggered when a contact is created"
  },
  {
    "event_type": "contact.updated",
    "description": "Triggered when a contact is updated"
  },
  {
    "event_type": "contact.deleted",
    "description": "Triggered when a contact is deleted"
  },
  {
    "event_type": "contact.label.added",
    "description": "Triggered when a label is added to a contact"
  },
  {
    "event_type": "contact.label.deleted",
    "description": "Triggered when a label is removed from a contact"
  }
]

```

## Test Your Webhook and know what will be sent

Simulate different types of events to validate your webhook endpoint. This
section walks you through:

- How test requests are constructed
- What payload structure to expect

#### Endpoint

`POST /api/v1/workspaces/{workspace_id}/test`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Name        | Type   | Required | Description                                             |
| ----------- | ------ | -------- | ------------------------------------------------------- |
| event_type  | string | Yes      | The type of event to simulate (e.g. `conversation.new`) |
| webhook_url | string | Yes      | The URL to which the test payload will be sent          |

#### Sample Request

```bash
curl -X POST "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/test" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "conversation.new",
    "webhook_url": "https://api.example.com/test-webhook"
  }'
```

## View Delivery Logs

Learn how to retrieve delivery logs for your webhooks and what you can expect in
logs.

### Get Webhook Delivery Logs for a Workspace

Retrieves webhook delivery logs for a specific workspace. You can optionally
filter results by event type, delivery status, date range, and more.

#### Endpoint

`GET /api/v1/workspaces/{workspace_id}/logs`

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

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

##### Successful Response

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

### Get Webhook Delivery Logs for a Subscription

Retrieve webhook delivery logs tied to a specific subscription. Supports
optional filtering by event type, delivery status, date range, ordering, and
pagination.

#### Endpoint

`GET /api/v1/workspaces/{workspace_id}/logs/{subscription_id}`

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

```bash
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/{subscription_id}?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

##### Successful Response

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

### Export Webhook Delivery Logs to Email

Export webhook delivery logs for a workspace within a specific date range and
receive a download link via email.

#### Endpoint

`POST /api/v1/workspaces/{workspace_id}/logs/export`

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

##### Successful Response

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
