---
title: Bulk SMS/MMS Campaigns
linkTitle: Bulk SMS/MMS Campaigns
description:
  API endpoints for creating and managing bulk SMS/MMS campaigns with contact
  targeting and scheduling.
categories: [API, Bulk SMS Campaign, SMS Campaign, MMS Campaign]
tags: [bulk sms, mms, campaign, messaging, contacts]
type: docs
weight: 3
---

# Bulk SMS/MMS Campaigns

## Overview

The Bulk SMS/MMS Campaigns API enables you to send messages at scale to targeted
contact lists. This comprehensive guide covers contact management, campaign
creation, and monitoring. The API supports SMS, MMS, and WhatsApp Business
Platform messages with advanced targeting, scheduling, and delivery tracking
capabilities.

After reading through this tutorial, try out the endpoints
[here](./Docs/seax-api/)

## Authorization

You must provide your API key in the `X-API-KEY` header.

To set up your API Key:

- Go to **Account → API Key** tab.
- Refresh the Key if needed
- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

## Step-by-Step Guide

### 1. Get Phone Numbers

`GET /api/v1/workspace/{workspace_id}/phones`

First, retrieve available phone numbers for sending campaigns.

| Field          | Type              | Description                                                          | Allowed Values / Example               | Required |
| -------------- | ----------------- | -------------------------------------------------------------------- | -------------------------------------- | -------- |
| `X-API-Key`    | `string (header)` | API key for authorization. See [Authorization Guide](#authorization) | `<your_api_key>`                       | ✅       |
| `workspace_id` | `string (path)`   | Unique identifier of the workspace                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `offset`       | `integer (query)` | Number of results to skip before starting to return.<br>Default: 0   | `0`                                    |          |
| `limit`        | `integer (query)` | Max number of results to return.<br>Default: 10                      | `10`                                   |          |
| `is_owned`     | `boolean (query)` | Filter for owned records only.<br>Default: `false`                   | `true`, `false`                        |          |
| `enabled`      | `boolean (query)` | Filter by whether the item is enabled.<br>Default: `true`            | `true`, `false`                        |          |

###### Example

Request:

```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/phones?offset=0&limit=10&is_owned=false&enabled=true' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response:

```json
{
  "data": [
    {
      "name": "Marketing Line",
      "enabled": true,
      "phone": "+1234567890",
      "country": "US",
      "type": "LOCAL",
      "source": "TWILIO",
      "phone_capability": {
        "sms": true,
        "mms": true,
        "voice": true,
        "fax": false
      },
      "is_default": true,
      "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
      "created_time": "2025-07-07T18:12:58.351633",
      "updated_time": "2025-07-07T18:12:58.351649"
    }
  ],
  "total": 1
}
```

### 2. Get Contacts

`GET /api/v1/workspace/{workspace_id}/contacts`

Retrieve and filter contacts to target in your campaign.

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

Response:

```json
{
  "data": [
    {
      "name": "John Doe",
      "phone": "+12345678900",
      "note": "VIP customer",
      "whatsapp_phone": "+12345678900",
      "contact_field_data": {
        "customer_tier": "gold",
        "last_purchase": "2024-01-15"
      },
      "id": "11111111-2222-4444-3333-555555555555",
      "workspace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "created_time": "2025-07-07T18:13:04.845276",
      "updated_time": "2025-07-07T18:13:04.845287",
      "contact_labels": [
        {
          "name": "vip_customers",
          "color": "#19b9c3",
          "description": "VIP customers with high lifetime value",
          "id": "11111111-2222-4444-3333-555555555555",
          "is_system": false
        }
      ]
    }
  ],
  "total": 1
}
```

### 3. Import Contacts (Optional)

`POST /api/v1/workspace/{workspace_id}/import_contacts`

Import contacts from a CSV file if you need to add new contacts.

| Field                | Type               | Description                                                          | Allowed Values / Example               | Required |
| -------------------- | ------------------ | -------------------------------------------------------------------- | -------------------------------------- | -------- |
| `X-API-Key`          | `string (header)`  | API key for authorization. See [Authorization Guide](#authorization) | `<your_api_key>`                       | ✅       |
| `workspace_id`       | `string (path)`    | Unique identifier of the workspace                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `file`               | `file (form-data)` | CSV file containing contacts                                         | `contacts.csv`                         | ✅       |
| `duplicate_strategy` | `string (query)`   | How to handle duplicate contacts                                     | `mark`, `skip`, `update`               |          |
| `phone_country`      | `string (query)`   | Default country code for phone numbers                               | `US`, `GB`, `CA`                       |          |

###### Example

Request:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/import_contacts?duplicate_strategy=mark&phone_country=US' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>' \
  -F 'file=@contacts.csv'
```

Response:

```json
{
  "id": "job_12345678-abcd-efgh-ijkl-123456789012",
  "status": "processing",
  "job_type": "import_contacts",
  "created_time": "2025-07-17T19:00:00.000Z",
  "updated_time": "2025-07-17T19:00:00.000Z",
  "progress": 0,
  "total_items": 1000,
  "processed_items": 0,
  "failed_items": 0
}
```

### 4. Create Bulk SMS/MMS Campaign

`POST /api/v1/workspace/{workspace_id}/campaigns`

**IMPORTANT**: This endpoint will immediately send the campaign to all selected
contacts. Carefully select your target audience using contact labels.

| Field                           | Type                  | Description                                                          | Allowed Values / Example                                                                  | Required |
| ------------------------------- | --------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------- |
| `X-API-Key`                     | `string (header)`     | API key for authorization. See [Authorization Guide](#authorization) | `<your_api_key>`                                                                          | ✅       |
| `workspace_id`                  | `string (path)`       | Unique identifier of the workspace                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                                    | ✅       |
| `name`                          | `string`              | Campaign name                                                        | `Spring Sale 2025`                                                                        | ✅       |
| `type`                          | `string`              | Campaign type                                                        | `SMS`, `MMS`, `AI_AGENT`, `WHATSAPP_BUSINESS_PLATFORM_MESSAGE`                            | ✅       |
| `message`                       | `string`              | Message content                                                      | `🌸 Spring Sale Alert! Get 25% off all items. Use code SPRING25. Valid until March 31st.` | ✅       |
| `phone_ids`                     | `array[string]`       | Phone number IDs to send from                                        | `["020086f5-fb0e-4a0c-920a-bbdd04f4381c"]`                                                | ✅       |
| `any_contact_label_ids`         | `array[string]`       | Include contacts with any of these labels                            | `["11111111-2222-4444-3333-555555555555"]`                                                |          |
| `all_contact_label_ids`         | `array[string]`       | Include contacts with all of these labels                            | `["22222222-3333-5555-4444-666666666666"]`                                                |          |
| `exclude_contact_ids`           | `array[string]`       | Exclude specific contact IDs                                         | `["11111111-2222-4444-3333-555555555555"]`                                                |          |
| `exclude_any_contact_label_ids` | `array[string]`       | Exclude contacts with any of these labels                            | `["33333333-4444-6666-5555-777777777777"]`                                                |          |
| `media_urls`                    | `array[string]`       | Media URLs for MMS campaigns                                         | `["https://example.com/image.jpg"]`                                                       |          |
| `start_time`                    | `string ($date-time)` | Campaign start time (for scheduling)                                 | `2025-07-18T10:00:00+00:00`                                                               |          |
| `end_time`                      | `string ($date-time)` | Campaign end time (for scheduling)                                   | `2025-07-18T18:00:00+00:00`                                                               |          |
| `is_schedule`                   | `boolean`             | Whether the campaign is scheduled                                    | `true`, `false`                                                                           |          |
| `enable_link_shortening`        | `boolean`             | Enable automatic link shortening in messages                         | `true`, `false`                                                                           |          |
| `attach_contact_label_ids`      | `array[string]`       | Labels to attach to contacts after campaign                          | `["spring_campaign_2025"]`                                                                |          |

###### Example: SMS Campaign

Request:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <your_api_key>' \
  -d '{
    "name": "Spring Sale 2025",
    "type": "SMS",
    "message": "🌸 Spring Sale Alert! Get 25% off all items. Use code SPRING25. Valid until March 31st. Shop now: https://example.com/sale",
    "phone_ids": ["020086f5-fb0e-4a0c-920a-bbdd04f4381c"],
    "any_contact_label_ids": ["11111111-2222-4444-3333-555555555555"],
    "exclude_any_contact_label_ids": ["22222222-3333-5555-4444-666666666666"],
    "enable_link_shortening": true,
    "attach_contact_label_ids": ["33333333-4444-6666-5555-777777777777"],
    "is_schedule": false
  }'
```

Response:

```json
{
  "id": "campaign_12345678-abcd-efgh-ijkl-123456789012",
  "name": "Spring Sale 2025",
  "type": "SMS",
  "message": "🌸 Spring Sale Alert! Get 25% off all items. Use code SPRING25. Valid until March 31st. Shop now: https://example.com/sale",
  "status": "sending",
  "created_time": "2025-07-17T19:00:00.000Z",
  "updated_time": "2025-07-17T19:00:00.000Z",
  "start_time": "2025-07-17T19:00:00.000Z",
  "phones": [
    {
      "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
      "phone": "+1234567890",
      "name": "Marketing Line"
    }
  ],
  "target_contact_count": 1250,
  "job_id": "job_12345678-abcd-efgh-ijkl-123456789012"
}
```

###### Example: MMS Campaign

Request:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <your_api_key>' \
  -d '{
    "name": "New Product Launch",
    "type": "MMS",
    "message": "Introducing our latest product! Check out the image and visit our store.",
    "media_urls": ["https://example.com/product-image.jpg"],
    "phone_ids": ["020086f5-fb0e-4a0c-920a-bbdd04f4381c"],
    "any_contact_label_ids": ["product_enthusiasts"],
    "is_schedule": false
  }'
```

### 5. Monitor Campaign Progress

`GET /api/v1/workspace/{workspace_id}/campaigns/{campaign_id}`

Get detailed information about a specific campaign.

| Field          | Type              | Description                                                          | Allowed Values / Example                        | Required |
| -------------- | ----------------- | -------------------------------------------------------------------- | ----------------------------------------------- | -------- |
| `X-API-Key`    | `string (header)` | API key for authorization. See [Authorization Guide](#authorization) | `<your_api_key>`                                | ✅       |
| `workspace_id` | `string (path)`   | Unique identifier of the workspace                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6`          | ✅       |
| `campaign_id`  | `string (path)`   | Unique identifier of the campaign                                    | `campaign_12345678-abcd-efgh-ijkl-123456789012` | ✅       |

###### Example

Request:

```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns/campaign_12345678-abcd-efgh-ijkl-123456789012' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response:

```json
{
  "id": "campaign_12345678-abcd-efgh-ijkl-123456789012",
  "name": "Spring Sale 2025",
  "type": "SMS",
  "status": "finished",
  "message": "🌸 Spring Sale Alert! Get 25% off all items. Use code SPRING25. Valid until March 31st. Shop now: https://example.com/sale",
  "created_time": "2025-07-17T19:00:00.000Z",
  "updated_time": "2025-07-17T19:15:00.000Z",
  "start_time": "2025-07-17T19:00:00.000Z",
  "end_time": "2025-07-17T19:15:00.000Z",
  "statistics": {
    "total_contacts": 1250,
    "sent": 1245,
    "failed": 5,
    "delivered": 1200,
    "bounced": 45,
    "opened": 890,
    "clicked": 234
  },
  "phones": [
    {
      "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
      "phone": "+1234567890",
      "name": "Marketing Line"
    }
  ]
}
```

### 6. Get Campaign Logs

`GET /api/v1/workspace/{workspace_id}/campaigns/{campaign_id}/logs`

Retrieve detailed logs for individual message deliveries.

| Field              | Type              | Description                                                          | Allowed Values / Example                        | Required |
| ------------------ | ----------------- | -------------------------------------------------------------------- | ----------------------------------------------- | -------- |
| `X-API-Key`        | `string (header)` | API key for authorization. See [Authorization Guide](#authorization) | `<your_api_key>`                                | ✅       |
| `workspace_id`     | `string (path)`   | Unique identifier of the workspace                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6`          | ✅       |
| `campaign_id`      | `string (path)`   | Unique identifier of the campaign                                    | `campaign_12345678-abcd-efgh-ijkl-123456789012` | ✅       |
| `message_statuses` | `string (query)`  | Filter by message status                                             | `sent,delivered,failed`                         |          |
| `offset`           | `integer (query)` | Number of rows to skip.<br>Default: `0`                              | `0`                                             |          |
| `limit`            | `integer (query)` | Number of rows to return.<br>Default: `10`                           | `10`                                            |          |

###### Example

Request:

```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns/campaign_12345678-abcd-efgh-ijkl-123456789012/logs?offset=0&limit=10&message_statuses=delivered,failed' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response:

```json
{
  "data": [
    {
      "id": "log_12345678-abcd-efgh-ijkl-123456789012",
      "contact_id": "11111111-2222-4444-3333-555555555555",
      "contact_name": "John Doe",
      "contact_phone": "+12345678900",
      "message_status": "delivered",
      "sent_time": "2025-07-17T19:01:00.000Z",
      "delivered_time": "2025-07-17T19:01:30.000Z",
      "error_message": null,
      "message_id": "msg_12345678-abcd-efgh-ijkl-123456789012"
    },
    {
      "id": "log_87654321-dcba-hgfe-lkji-210987654321",
      "contact_id": "22222222-3333-5555-4444-666666666666",
      "contact_name": "Jane Smith",
      "contact_phone": "+19876543210",
      "message_status": "failed",
      "sent_time": "2025-07-17T19:01:00.000Z",
      "delivered_time": null,
      "error_message": "Invalid phone number",
      "message_id": "msg_87654321-dcba-hgfe-lkji-210987654321"
    }
  ],
  "total": 1245,
  "offset": 0,
  "limit": 10
}
```

### 7. Send Individual Messages

`POST /api/v1/workspace/{workspace_id}/send_message`

For sending individual messages to specific contacts (not bulk campaigns).

| Field             | Type              | Description                                                          | Allowed Values / Example               | Required |
| ----------------- | ----------------- | -------------------------------------------------------------------- | -------------------------------------- | -------- |
| `X-API-Key`       | `string (header)` | API key for authorization. See [Authorization Guide](#authorization) | `<your_api_key>`                       | ✅       |
| `workspace_id`    | `string (path)`   | Unique identifier of the workspace                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `phone_number`    | `string`          | Sender phone number                                                  | `+1234567890`                          | ✅       |
| `to_phone_number` | `string`          | Recipient phone number                                               | `+19876543210`                         | ✅       |
| `content`         | `string`          | Message content                                                      | `Thank you for your recent purchase!`  | ✅       |
| `media_urls`      | `array[string]`   | Media URLs for MMS messages                                          | `["https://example.com/receipt.jpg"]`  |          |

###### Example

Request:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/send_message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <your_api_key>' \
  -d '{
    "phone_number": "+1234567890",
    "to_phone_number": "+19876543210",
    "content": "Thank you for your recent purchase! Your order #12345 has been shipped."
  }'
```

Response:

```json
{
  "id": "msg_12345678-abcd-efgh-ijkl-123456789012",
  "status": "sent",
  "from_phone": "+1234567890",
  "to_phone": "+19876543210",
  "content": "Thank you for your recent purchase! Your order #12345 has been shipped.",
  "created_time": "2025-07-17T19:00:00.000Z",
  "sent_time": "2025-07-17T19:00:01.000Z"
}
```

## Best Practices

### Contact Targeting

1. **Use Labels Effectively**: Organize contacts with meaningful labels like
   `vip_customers`, `new_subscribers`, `location_nyc`
2. **Exclude DNC Lists**: Always exclude `DNC` (Do Not Contact) and
   `unsubscribed` labels
3. **Test with Small Groups**: Test campaigns with a small subset before sending
   to large audiences
4. **Segment by Engagement**: Use labels to track engagement levels and target
   accordingly

### Message Content

1. **Keep It Concise**: SMS messages have character limits; be clear and direct
2. **Include Clear CTAs**: Use clear calls-to-action with shortened links
3. **Personalization**: Use contact fields for personalized messaging
4. **Timing**: Consider time zones and send during appropriate hours

### Campaign Management

1. **Monitor Delivery**: Check campaign logs regularly for delivery issues
2. **Track Performance**: Monitor open rates, click rates, and conversions
3. **Handle Failures**: Review failed messages and update contact information
4. **Respect Opt-outs**: Process unsubscribe requests immediately

## Error Handling

Common error responses and how to handle them:

### Authentication Errors

```json
{
  "error": "Unauthorized",
  "message": "Invalid API key",
  "status_code": 401
}
```

### Validation Errors

```json
{
  "error": "Validation Error",
  "message": "Invalid phone number format",
  "status_code": 422,
  "details": {
    "field": "to_phone_number",
    "code": "INVALID_FORMAT"
  }
}
```

### Rate Limit Errors

```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests",
  "status_code": 429,
  "retry_after": 60
}
```

## Conclusion

The SeaX Bulk SMS/MMS API provides powerful tools for managing large-scale
messaging campaigns. By following this guide, you can effectively target
contacts, send campaigns, and monitor performance. Remember to always respect
customer preferences and maintain compliance with messaging regulations.
