---
title: Notifications on Contact Label Changes Event
linkTitle: Contact Label Changes Notification
description:
  Learn how to receive notifications when contact labels are added or deleted
  using the SeaX API.
type: docs
weight: 9
---

# Manage Contact Labels on Contacts

## Overview

This guide shows how to:

- Retrieve all contact labels in a workspace
- Attach, detach, or replace labels on a specific contact

After reading through this tutorial, try out the endpoints
[here](./Docs/seax-api/)

There are two ways to create webhook subscriptions in SeaX.

## **Option 1 – Using the SeaX UI**

1. Log in to your SeaX account.
2. From the left-hand menu, navigate to **Workspace → Events**.
3. Click **Add a New Subscription**.
4. Enter your webhook destination URL.
5. Toggle on the event types you want to subscribe to (for example,
   `contact.label.added` and `contact.label.deleted`).
6. Click **Save**.

Your webhook is now subscribed to those events. Whenever one of the selected
events occurs—such as when a **DNC** label is applied to a contact—SeaX will
automatically send a notification to your webhook URL.

## **Option 2 – Using the API**

You can also create and manage webhook subscriptions programmatically through
the SeaX API. [This link](https://seax.seasalt.ai/notify-api/redoc/) contains a
general and comprehensive tutorial for this set of API endpoints. Use the
subscription endpoint to register your webhook destination and specify the event
types you want to receive.

## Authorization: API Key

Ensure the following are in place:

### **1\. Generate Your API Key**

All APIs require a valid API key issued from your workspace. All requests must
include a valid API key in the request header (`X-API-Key`).

- Go to **Workspace → API Key** tab.

- Click **Add New Key** and check `Workspace Events Notification` as the scope.

- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

### **2\. Prepare Your Webhook Receiver**

Your server must:

- Be publicly accessible over **HTTPS**

- Accept **POST** requests

- Handle **application/json** payloads

## API Specification

This section explains how to manage webhook subscriptions in your workspace.

### **Create a Subscription**

Create a new webhook subscription in your SeaX workspace.

#### Endpoint

`POST https://seax.seasalt.ai/notify-api/v1/workspaces/{workspace_id}/subscription`

Use this endpoint to register a webhook that will receive event notifications
from SeaX.

#### Authorization

You must provide your API key in the `X-API-KEY` header.

#### Request Body

| Field         | Type              | Required | Description                                                           |
| :------------ | :---------------- | :------- | :-------------------------------------------------------------------- |
| `webhook_url` | `string`          | ✅       | The publicly accessible URL to receive webhook events.                |
| `event_types` | `array of string` | ✅       | List of event types to subscribe to. See supported event types below. |
| `created_by`  | `string`          |          | Identifier of the user creating the subscription.                     |
| `is_enabled`  | `boolean`         | ✅       | Whether the subscription is active (`true`) or paused (`false`).      |
| `type`        | `string`          |          | Subscription source. Options: `"SEASALT"` (default), `"ZAPIER"`       |

**Supported Event Types**

To get a list of supported event types, you can use
[this endpoint](#get-a-list-of-supported-events).

- **`contact.label.added`**
- **`contact.label.deleted`**

These are the two event types you want to subscribe to get notification when
contact labels are changed.

**Sample Request**

```bash
curl -X POST "https://seax.seasalt.ai/notify-api/v1/workspaces/{workspace_id}/subscription" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://api.example.com/webhook",
    "event_types": ["contact.label.added", "contact.label.deleted"],
    "created_by": "user_12345",
    "is_enabled": true,
    "type": "SEASALT"
  }'
```

**Sample Successful Response**

```bash
{
  "webhook_url": "https://api.example.com/webhook",
  "event_types": ["contact.label.added", "contact.label.deleted"],
  "created_by": "user_12345",
  "is_enabled": true,
  "type": "SEASALT"
}
```

To know more about how to retrieve, update or delete your subscriptions, read
the full API tutorial here:
[Event Notification API Swagger](https://seax.seasalt.ai/notify-api/redoc/)

## **Test Your Webhook and Know What Will Be Sent**

Simulate different types of events to validate your webhook endpoint. This
section walks you through:

- How test requests are constructed
- What payload structure to expect

#### Endpoint

`POST https://seax.seasalt.ai/notify-api/v1/workspaces/{workspace_id}/test`

#### Authorization

This endpoint requires an API key passed in the `X-API-KEY` header.

#### Request Body

| Name        | Type   | Required | Description                                                                         |
| ----------- | ------ | -------- | ----------------------------------------------------------------------------------- |
| event_type  | string | Yes      | The type of event to simulate (e.g. `contact.label.added`, `contact.label.deleted`) |
| webhook_url | string | Yes      | The URL to which the test payload will be sent                                      |

**Sample Request**

```bash
curl -X POST "https://seax.seasalt.ai/notify-api/v1/workspaces/{workspace_id}/test" \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "contact.label.added",
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
    "event_type": "contact.label.added",
    "workspace": {
        "id": "workspace-123",
        "name": "Test Workspace"
    },
    "data": {
        "contact_id": str(uuid.uuid4()),
        "contact_name": "Zapier Contact",
        "updated_fields": [
            "labels"
        ],
        "previous": {
            "labels": [
                {
                    "id": "8d99e9b041f04447858cde7506cee4d5",
                    "name": "newUser",
                    "type": "CONTACT",
                    "color": "#565e9c",
                    "is_system": False,
                    "description": "this is a new user",
                }
            ]
        },
        "current": {
            "labels": [
                {
                    "id": "8d99e9b041f04447858cde7506cee4d5",
                    "name": "newUser",
                    "type": "CONTACT",
                    "color": "#565e9c",
                    "is_system": False,
                    "description": "this is a new user",
                },
                {
                    "id": "90c51757408941e2834f76392249b10f",
                    "name": "DNC",
                    "type": "CONTACT",
                    "color": "#a7927f",
                    "is_system": True,
                    "description": "",
                },
            ]
        },
        "labels": [
            {
                "id": "90c51757408941e2834f76392249b10f",
                "name": "DNC",
                "type": "CONTACT",
                "color": "#a7927f",
                "is_system": True,
                "description": "",
            }
        ],
    },
    "subscription_created_by": "Test_user",
    "subscription_updated_by": "Test_user"
}
```

## Step-by-Step Guide

### 1) Get Contact Labels

`GET /api/v1/workspace/{workspace_id}/contact_labels`

List all contact labels available in your workspace. Use these label IDs when
updating a contact or interpreting `contact.label.*` webhook events.

| Field                      | Type              | Description                                                            | Allowed Values / Example               | Required |
| -------------------------- | ----------------- | ---------------------------------------------------------------------- | -------------------------------------- | -------- |
| `X-API-Key`                | `string (header)` | API key for authorization (see Authorization)                          | `<your_api_key>`                       |          |
| `workspace_id`             | `string (path)`   | Workspace ID                                                           | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `keyword`                  | `string (query)`  | Optional, determine the keyword to search contact names and phones.    | `+18111222333`                         |          |
| `offset`                   | `integer (query)` | Rows to skip                                                           | `0`                                    |          |
| `limit`                    | `integer (query)` | Max rows to return (0 = all)                                           | `10`                                   |          |
| `order_by`                 | `string (query)`  | Sort by comma-separated `<field>:<direction>` pairs                    | `name:desc` (default)                  |          |
| `is_system`                | `boolean (query)` | Filter by system labels                                                | `true`/`false`                         |          |
| `exclude_labels`           | `string (query)`  | Exclude labels (comma-separated names)                                 | `invalid number,unreachable`           |          |
| `exclude_labels_for_count` | `string (query)`  | Exclude labels when calculating contact counts (comma-separated names) | `DNC,invalid number,unreachable`       |          |
| `contact_counting`         | `boolean (query)` | Return contact count per label (default: true)                         | `true`/`false`                         |          |
| `whatsapp_phone_only`      | `boolean (query)` | Only include contacts that have WhatsApp phone when counting           | `true`/`false`                         |          |
| `phone_only`               | `boolean (query)` | Only include contacts that have a phone when counting                  | `true`/`false`                         |          |

###### Example

Request:

```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/contact_labels?keyword=VIP&offset=0&limit=10&order_by=name:desc&contact_counting=true&phone_only=false&whatsapp_phone_only=false' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response:

```json
{
  "data": [
    {
      "id": "11111111-2222-4444-3333-555555555555",
      "name": "vip_customers",
      "type": "CONTACT",
      "color": "#19b9c3",
      "is_system": false,
      "description": "VIP customers with high lifetime value",
      "contact_count": 42
    },
    {
      "id": "33333333-4444-6666-5555-777777777777",
      "name": "dnc",
      "type": "CONTACT",
      "color": "#FF4D4F",
      "is_system": true,
      "description": "Do Not Contact",
      "contact_count": 5
    }
  ],
  "total": 2,
  "offset": 0,
  "limit": 10
}
```

### 2) Get a list of contacts of your workspace

`GET /api/v1/workspace/{workspace_id}/contacts`

List contacts and obtain `contact_id` values to use with the update endpoint and
to interpret `contact.label.*` webhooks.

| Field                           | Type              | Description                                                                                  | Allowed Values / Example                                                    | Required |
| ------------------------------- | ----------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | -------- |
| `X-API-Key`                     | `string (header)` | Authorization with APIKey                                                                    | `<your_api_key>`                                                            |          |
| `workspace_id`                  | `string (path)`   | Workspace ID                                                                                 | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                      | ✅       |
| `offset`                        | `integer (query)` | Optional, number of rows to skip                                                             | `0`                                                                         |          |
| `limit`                         | `integer (query)` | Optional, number of rows to return after offset (0 = all)                                    | `10`                                                                        |          |
| `keyword`                       | `string (query)`  | Optional, keyword to search contact names and phones                                         | `+18111222333`                                                              |          |
| `whatsapp_phone`                | `string (query)`  | Optional, search contacts by exact WhatsApp phone                                            | `+18111222333`                                                              |          |
| `all_contact_label_ids`         | `string (query)`  | Optional, contacts must match all label IDs (comma-separated UUIDs)                          | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666` |          |
| `any_contact_label_ids`         | `string (query)`  | Optional, contacts match any label IDs (comma-separated UUIDs)                               | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666` |          |
| `exclude_contact_ids`           | `string (query)`  | Optional, exclude contacts by IDs (comma-separated UUIDs)                                    | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666` |          |
| `exclude_any_contact_label_ids` | `string (query)`  | Optional, exclude contacts that match any of these label IDs (comma-separated UUIDs)         | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666` |          |
| `exclude_all_contact_label_ids` | `string (query)`  | Optional, exclude contacts that match all of these label IDs (comma-separated UUIDs)         | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666` |          |
| `addition_contact_ids`          | `string (query)`  | Optional, force-include these contacts in result (comma-separated UUIDs)                     | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666` |          |
| `order_by`                      | `string (query)`  | Optional, comma-separated list of `<field>:<direction>` pairs (default: `created_time:desc`) | `phone:asc,created_time:desc,name:asc`                                      |          |
| `exclude_labels`                | `string (query)`  | Optional, exclude by label names (comma-separated). Affects label-based filtering and counts | `DNC,invalid number,unreachable`                                            |          |
| `whatsapp_phone_only`           | `boolean (query)` | Optional, only include contacts that match whatsapp_phone                                    | `false`                                                                     |          |
| `phone_only`                    | `boolean (query)` | Optional, only include contacts that have a phone number                                     | `false`                                                                     |          |

###### Example

Request:

```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/contacts?offset=0&limit=10&keyword=%2B18111222333&any_contact_label_ids=11111111-2222-4444-3333-555555555555&exclude_labels=DNC,invalid%20number' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response (truncated):

```json
{
  "data": [
    {
      "id": "11111111-2222-4444-3333-555555555555",
      "name": "John Doe",
      "phone": "+12345678900",
      "whatsapp_phone": "+12345678900",
      "contact_labels": [
        {
          "id": "11111111-2222-4444-3333-555555555555",
          "name": "vip_customers",
          "is_system": false
        }
      ]
    }
  ],
  "total": 1
}
```

### 3) Update a Contact's Labels

`PATCH /api/v1/workspace/{workspace_id}/contacts/{contact_id}`

Update a contact. You can update core fields (name, phones, note), custom field
data, and contact labels. For labels, you can either:

- Attach labels (add without affecting existing ones)
- Detach labels (remove specific ones)
- Replace all labels (set the exact list of labels the contact should have)

Path/Header

| Field          | Type              | Description               | Example                                | Required |
| -------------- | ----------------- | ------------------------- | -------------------------------------- | -------- |
| `X-API-Key`    | `string (header)` | Authorization with APIKey | `<your_api_key>`                       |          |
| `workspace_id` | `string (path)`   | Workspace ID              | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `contact_id`   | `string (path)`   | Contact ID                | `11111111-2222-4444-3333-555555555555` | ✅       |

Request Body: UpdateContact

| Field                | Type            | Description                                                                                                                     | Example                                    |
| -------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `name`               | `string`        | Contact name                                                                                                                    | `"John Doe"`                               |
| `phone`              | `string`        | Primary phone number (E.164 recommended)                                                                                        | `"+12345678900"`                           |
| `whatsapp_phone`     | `string`        | WhatsApp phone number (E.164)                                                                                                   | `"+12345678900"`                           |
| `note`               | `string`        | Freeform note                                                                                                                   | `"VIP customer"`                           |
| `contact_field_data` | `object`        | Custom key-value fields                                                                                                         | `{ "last_purchase": "2024-01-15" }`        |
| `contact_label_ids`  | `array[string]` | Replace the contact's labels with exactly this set (mutually exclusive with attach/detach).                                     | `["22222222-3333-5555-4444-666666666666"]` |
| `replace_all_labels` | `boolean`       | Default: false If true, completely replace all labels including system labels. If false (default), system labels are preserved. | `false`                                    |

Notes:

- Provide `contact_label_ids` to replace all labels.
- Unknown or invalid label IDs will cause a validation error.
- System labels are: `DNC`, `invalid number`, `unreachable`, and `duplicate`.

###### Example: replace labels

Request:

```bash
curl -X 'PATCH' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/contacts/11111111-2222-4444-3333-555555555555' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28' \
  -d '{
    "contact_label_ids": [
      "11111111-2222-4444-3333-555555555555",
      "22222222-3333-5555-4444-666666666666"
    ]
  }'
```

Response:

```json
{
  "id": "9999999-2222-4444-3333-888888888888",
  "name": "John Doe",
  "phone": "+12345678900",
  "contact_labels": [
    {
      "name": "vip_customers",
      "color": "#19b9c3",
      "description": "VIP customers with high lifetime value",
      "id": "11111111-2222-4444-3333-555555555555",
      "is_system": false
    },
    {
      "name": "recent_buyers",
      "color": "#6BB700",
      "description": "Purchased within last 30 days",
      "id": "22222222-3333-5555-4444-666666666666",
      "is_system": false
    }
  ],
  "updated_time": "2025-07-17T19:00:00.000Z"
}
```
