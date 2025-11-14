---
title: Notifications on Contact Label Changes Event
linkTitle: Contact Label Changes Notification
description:
  Learn how to receive notifications when contact labels are added or deleted
  using the SeaX API.
type: docs
weight: 11
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
