---
title: WhatsApp Business Platform Campaigns
linkTitle: WhatsApp Business Platform Campaigns
description: API endpoints for setting up and managing campaigns via the WhatsApp Business Platform.
categories: [API, WhatsApp Campaign, Messaging, Campaign Management]
tags: [whatsapp, business platform, campaign, messaging, contacts]
type: docs
weight: 25
---

# WhatsApp Business Platform Campaigns

## Overview

The WhatsApp Business Platform Campaigns API empowers organizations to design and implement effective messaging campaigns targeting contacts on WhatsApp. By leveraging this platform, businesses can engage their audience on a widely-used messaging app, increasing open rates and enhancing customer interactions.

### Key Benefits
- **Wider Reach**: Connect with billions of users worldwide.
- **Personalization**: Customize messages to maximize engagement.
- **Rich Media**: Send images, videos, and documents.
- **Automation**: Schedule and automate messaging workflows.

### Use Cases
- Product Promotions
- Customer Feedback Campaigns
- Announcements and Updates

### Limitations
- Requires a verified business account.
- Limited to contacts who have opted-in.

After reading through this tutorial, try out the endpoints [here](./Docs/bulk-sms-api/)

## Getting Started

### Authorization

To interact with the WhatsApp Business Platform Campaigns API, you need to authorize your requests using an API key, which must be included in the `X-API-KEY` header for every request.

#### Setting Up Your API Key
1. Navigate to **Account → API Key** tab in your dashboard.
2. Generate or refresh your API Key if necessary.
3. Copy the API Key and store it securely.

> **Note**: Keep your API key confidential to ensure the security of your service.

Example Header:
```bash
-H 'X-API-Key: your_api_key_here'
```

For more details on authorization, refer to the [Authorization Guide](#authorization).

## Step-by-Step Guide

### 1. Retrieve Phone Numbers

**Endpoint**: `GET /api/v1/workspace/{workspace_id}/phones`

Begin by retrieving available phone numbers linked to your WhatsApp Business account. These numbers will be used as sender IDs in campaigns.

**Request Parameters**:
- `workspace_id`: Unique identifier for your workspace.
- Optional query params like `offset`, `limit`, `is_owned`, and `enabled` for filtered results.

**Example Request**:
```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/{workspace_id}/phones?offset=0&limit=10' \
  -H 'accept: application/json' \
  -H 'X-API-Key: your_api_key_here'
```

**Response**:
```json
{
  "data": [
    {
      "name": "Sales Line",
      "phone": "+11234567890",
      "id": "phone_id_string"
    }
  ],
  "total": 1
}
```

| Field           | Type               | Description                                                  | Allowed Values / Example                                   | Required |
|-----------------|--------------------|--------------------------------------------------------------|-------------------------------------------------------------|----------|
| `X-API-Key`     | `string (header)`  | API key for authorization.                                   | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`             | ✅        |
| `workspace_id`  | `string (path)`    | Unique identifier of the workspace                           | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                      | ✅        |
| `offset`        | `integer (query)`  | Number of results to skip. Default is 0.                     | `0`                                                         |          |
| `limit`         | `integer (query)`  | Max number of results to return. Default is 10.              | `10`                                                        |          |
| `is_owned`      | `boolean (query)`  | Filter for owned records only. Default is false.             | `true`, `false`                                             |          |
| `enabled`       | `boolean (query)`  | Filter by enabled status. Default is true.                   | `true`, `false`                                             |          |

### 2. Retrieve Contacts

**Endpoint**: `GET /api/v1/workspace/{workspace_id}/contacts`

Next, access your contact list that you wish to target with your WhatsApp campaign.

**Request Parameters**:
- `workspace_id`: Unique identifier for your workspace.
- Optional query params like `offset`, `limit`, and `keyword` for refined searches.

**Example Request**:
```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/contacts?offset=0&limit=10' \
  -H 'accept: application/json' \
  -H 'X-API-Key: your_api_key_here'
```

**Response**:
```json
{
  "data": [
    {
      "name": "John Doe",
      "phone": "+1234567890",
      "id": "contact_id_string"
    }
  ],
  "total": 1
}
```

| Field           | Type               | Description                                                  | Allowed Values / Example                                   | Required |
|-----------------|--------------------|--------------------------------------------------------------|-------------------------------------------------------------|----------|
| `X-API-Key`     | `string (header)`  | API key for authorization.                                   | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`             | ✅        |
| `workspace_id`  | `string (path)`    | Unique identifier of the workspace                           | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                      | ✅        |
| `offset`        | `integer (query)`  | Number of rows to skip. Default is 0.                        | `0`                                                         |          |
| `limit`         | `integer (query)`  | Number of rows to return. Default is 10.                     | `10`                                                        |          |
| `keyword`       | `string (query)`   | Search keyword for contact names.                            | `+18111222333`                                              |          |

### 3. Set Up WhatsApp Campaign

**Endpoint**: `POST /api/v1/workspace/{workspace_id}/campaigns`

**IMPORTANT**: This endpoint will immediately send the campaign to all selected contacts. Carefully select your target audience using contact labels.

To initiate a WhatsApp Business Platform campaign, you'll need to configure various parameters based on your targeting and messaging requirements.

| Field                          | Type                  | Description                                                                 | Allowed Values / Example                                                   | Required |
|--------------------------------|-----------------------|-----------------------------------------------------------------------------|----------------------------------------------------------------------------|---------|
| `X-API-Key`                   | `string (header)`     | API key for authorization. See [Authorization Guide](#authorization)      | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`         | ✅       |
| `workspace_id`                | `string (path)`       | Unique identifier of the workspace                                         | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                    | ✅       |
| `name`                        | `string`              | Campaign name                                                              | `WhatsApp Holiday Sale 2025`                                              | ✅       |
| `type`                        | `string`              | Campaign type                                                              | `WHATSAPP_BUSINESS_PLATFORM_MESSAGE`                                      | ✅       |
| `message`                     | `string`              | Message content                                                            | `🎉 Holiday Sale! Get 30% off all items. Use code HOLIDAY30. Valid until Dec 31st!` | ✅       |
| `phone_ids`                   | `array[string]`       | Phone number IDs to send from                                             | `["020086f5-fb0e-4a0c-920a-bbdd04f4381c"]`                               | ✅       |
| `any_contact_label_ids`       | `array[string]`       | Include contacts with any of these labels                                 | `["11111111-2222-4444-3333-555555555555"]`                               |          |
| `all_contact_label_ids`       | `array[string]`       | Include contacts with all of these labels                                 | `["22222222-3333-5555-4444-666666666666"]`                               |          |
| `exclude_contact_ids`         | `array[string]`       | Exclude specific contact IDs                                              | `["11111111-2222-4444-3333-555555555555"]`                               |          |
| `exclude_any_contact_label_ids`| `array[string]`      | Exclude contacts with any of these labels                                 | `["33333333-4444-6666-5555-777777777777"]`                               |          |
| `start_time`                  | `string ($date-time)` | Campaign start time (for scheduling)                                      | `2025-07-18T10:00:00+00:00`                                               |          |
| `end_time`                    | `string ($date-time)` | Campaign end time (for scheduling)                                        | `2025-07-18T18:00:00+00:00`                                               |          |
| `is_schedule`                 | `boolean`             | Whether the campaign is scheduled                                         | `true`, `false`                                                           |          |
| `enable_link_shortening`      | `boolean`             | Enable automatic link shortening in messages                             | `true`, `false`                                                           |          |
| `attach_contact_label_ids`    | `array[string]`       | Labels to attach to contacts after campaign                              | `["holiday_campaign_2025"]`                                               |          |

#### Example: Basic WhatsApp Campaign

Request:
```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28' \
  -d '{
    "name": "WhatsApp Holiday Sale 2025",
    "type": "WHATSAPP_BUSINESS_PLATFORM_MESSAGE",
    "message": "🎉 Holiday Sale! Get 30% off all items. Use code HOLIDAY30. Shop now: https://example.com/sale",
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
  "name": "WhatsApp Holiday Sale 2025",
  "type": "WHATSAPP_BUSINESS_PLATFORM_MESSAGE",
  "message": "🎉 Holiday Sale! Get 30% off all items. Use code HOLIDAY30. Shop now: https://example.com/sale",
  "status": "sending",
  "created_time": "2025-07-17T19:00:00.000Z",
  "updated_time": "2025-07-17T19:00:00.000Z",
  "start_time": "2025-07-17T19:00:00.000Z",
  "phones": [
    {
      "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
      "phone": "+1234567890",
      "name": "WhatsApp Business Line"
    }
  ],
  "target_contact_count": 850,
  "job_id": "job_12345678-abcd-efgh-ijkl-123456789012"
}
```

#### Example: Scheduled WhatsApp Campaign

Request:
```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28' \
  -d '{
    "name": "Weekend Flash Sale",
    "type": "WHATSAPP_BUSINESS_PLATFORM_MESSAGE",
    "message": "⚡ Flash Sale Alert! 48 hours only - 40% off everything!",
    "phone_ids": ["020086f5-fb0e-4a0c-920a-bbdd04f4381c"],
    "any_contact_label_ids": ["vip_customers"],
    "start_time": "2025-07-18T08:00:00+00:00",
    "end_time": "2025-07-18T20:00:00+00:00",
    "is_schedule": true,
    "enable_link_shortening": true
  }'
```

### 4. Monitor Campaign Progress

**Endpoint**: `GET /api/v1/workspace/{workspace_id}/campaigns/{campaign_id}`

Get detailed information about a specific campaign to track performance and delivery status.

| Field           | Type               | Description                                                                 | Allowed Values / Example                                                   | Required |
|-----------------|--------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------|
| `X-API-Key`     | `string (header)`  | API key for authorization. See [Authorization Guide](#authorization)     | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`        | ✅       |
| `workspace_id`  | `string (path)`    | Unique identifier of the workspace                                        | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                   | ✅       |
| `campaign_id`   | `string (path)`    | Unique identifier of the campaign                                         | `campaign_12345678-abcd-efgh-ijkl-123456789012`                          | ✅       |

#### Example

Request:
```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns/campaign_12345678-abcd-efgh-ijkl-123456789012' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28'
```

Response:
```json
{
  "id": "campaign_12345678-abcd-efgh-ijkl-123456789012",
  "name": "WhatsApp Holiday Sale 2025",
  "type": "WHATSAPP_BUSINESS_PLATFORM_MESSAGE",
  "status": "finished",
  "message": "🎉 Holiday Sale! Get 30% off all items. Use code HOLIDAY30. Shop now: https://example.com/sale",
  "created_time": "2025-07-17T19:00:00.000Z",
  "updated_time": "2025-07-17T19:15:00.000Z",
  "start_time": "2025-07-17T19:00:00.000Z",
  "end_time": "2025-07-17T19:15:00.000Z",
  "statistics": {
    "total_contacts": 850,
    "sent": 845,
    "failed": 5,
    "delivered": 820,
    "read": 680,
    "replied": 127
  },
  "phones": [
    {
      "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
      "phone": "+1234567890",
      "name": "WhatsApp Business Line"
    }
  ]
}
```

### 5. Get Campaign Logs

**Endpoint**: `GET /api/v1/workspace/{workspace_id}/campaigns/{campaign_id}/logs`

Retrieve detailed logs for individual message deliveries to understand specific delivery outcomes.

| Field                    | Type               | Description                                                                 | Allowed Values / Example                                                   | Required |
|--------------------------|--------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------|
| `X-API-Key`             | `string (header)`  | API key for authorization. See [Authorization Guide](#authorization)     | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`        | ✅       |
| `workspace_id`          | `string (path)`    | Unique identifier of the workspace                                        | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                   | ✅       |
| `campaign_id`           | `string (path)`    | Unique identifier of the campaign                                         | `campaign_12345678-abcd-efgh-ijkl-123456789012`                          | ✅       |
| `message_statuses`      | `string (query)`   | Filter by message status                                                  | `sent,delivered,failed`                                                  |          |
| `offset`                | `integer (query)`  | Number of rows to skip.<br>Default: `0`                                  | `0`                                                                       |          |
| `limit`                 | `integer (query)`  | Number of rows to return.<br>Default: `10`                               | `10`                                                                      |          |

#### Example

Request:
```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns/campaign_12345678-abcd-efgh-ijkl-123456789012/logs?offset=0&limit=10&message_statuses=delivered,failed' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28'
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
      "read_time": "2025-07-17T19:05:15.000Z",
      "error_message": null,
      "message_id": "wamid_12345678-abcd-efgh-ijkl-123456789012"
    },
    {
      "id": "log_87654321-dcba-hgfe-lkji-210987654321",
      "contact_id": "22222222-3333-5555-4444-666666666666",
      "contact_name": "Jane Smith",
      "contact_phone": "+19876543210",
      "message_status": "failed",
      "sent_time": "2025-07-17T19:01:00.000Z",
      "delivered_time": null,
      "read_time": null,
      "error_message": "User is not registered on WhatsApp Business Platform",
      "message_id": "wamid_87654321-dcba-hgfe-lkji-210987654321"
    }
  ],
  "total": 845,
  "offset": 0,
  "limit": 10
}
```

### 6. Import Contacts (Optional)

**Endpoint**: `POST /api/v1/workspace/{workspace_id}/import_contacts`

Import contacts from a CSV file if you need to add new contacts to your workspace.

| Field              | Type               | Description                                                                 | Allowed Values / Example                                                   | Required |
|-------------------|--------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------|
| `X-API-Key`       | `string (header)`  | API key for authorization. See [Authorization Guide](#authorization)     | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`        | ✅       |
| `workspace_id`    | `string (path)`    | Unique identifier of the workspace                                        | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                   | ✅       |
| `file`            | `file (form-data)` | CSV file containing contacts                                              | `whatsapp_contacts.csv`                                                  | ✅       |
| `duplicate_strategy` | `string (query)`| How to handle duplicate contacts                                          | `mark`, `skip`, `update`                                                 |          |
| `phone_country`   | `string (query)`   | Default country code for phone numbers                                   | `US`, `GB`, `CA`                                                         |          |

#### Example

Request:
```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/import_contacts?duplicate_strategy=mark&phone_country=US' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28' \
  -F 'file=@whatsapp_contacts.csv'
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
  "total_items": 500,
  "processed_items": 0,
  "failed_items": 0
}
```

### 7. Common Errors & Handling

Understanding typical error responses is key to troubleshooting:

#### Authentication Errors
```json
{
  "error": "Unauthorized",
  "message": "Invalid API Key",
  "status_code": 401
}
```
**Solution**: Verify and refresh your API Key.

#### Missing Parameters
```json
{
  "error": "Bad Request",
  "message": "Required field is missing",
  "status_code": 400
}
```
**Solution**: Ensure all required fields are included in your requests.

#### WhatsApp Business Platform Errors
```json
{
  "error": "WhatsApp Business Platform Error",
  "message": "Message template not approved",
  "status_code": 422,
  "details": {
    "field": "message",
    "code": "TEMPLATE_NOT_APPROVED"
  }
}
```
**Solution**: Use approved message templates or ensure your business account has the necessary permissions.

#### Rate Limit Errors
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests",
  "status_code": 429,
  "retry_after": 60
}
```
**Solution**: Wait for the specified retry period before making additional requests.

### 8. Send Individual WhatsApp Messages

**Endpoint**: `POST /api/v1/workspace/{workspace_id}/send_message/wabp_template_message`

For sending individual WhatsApp messages to specific contacts (not bulk campaigns).

| Field              | Type               | Description                                                                 | Allowed Values / Example                                                   | Required |
|-------------------|--------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------|
| `X-API-Key`       | `string (header)`  | API key for authorization. See [Authorization Guide](#authorization)     | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`        | ✅       |
| `workspace_id`    | `string (path)`    | Unique identifier of the workspace                                        | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                   | ✅       |
| `phone_number`    | `string`           | Sender WhatsApp Business phone number                                     | `+1234567890`                                                             | ✅       |
| `to_phone_number` | `string`           | Recipient WhatsApp phone number                                           | `+19876543210`                                                            | ✅       |
| `message`         | `string`           | Message content                                                           | `Thank you for your interest in our products!`                           | ✅       |
| `media_urls`      | `array[string]`    | Media URLs for rich media messages                                        | `["https://example.com/product-catalog.pdf"]`                           |          |

#### Example

Request:
```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/send_whatsapp_message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28' \
  -d '{
    "phone_number": "+1234567890",
    "to_phone_number": "+19876543210",
    "message": "Thank you for your recent inquiry! Here's our product catalog.",
    "media_urls": ["https://example.com/product-catalog.pdf"]
  }'
```

Response:
```json
{
  "id": "wamsg_12345678-abcd-efgh-ijkl-123456789012",
  "status": "sent",
  "from_phone": "+1234567890",
  "to_phone": "+19876543210",
  "message": "Thank you for your recent inquiry! Here's our product catalog.",
  "created_time": "2025-07-17T19:00:00.000Z",
  "sent_time": "2025-07-17T19:00:01.000Z"
}
```

## Best Practices

### Contact Targeting

1. **Use Labels Effectively**: Organize contacts with meaningful labels like `premium_customers`, `new_subscribers`, `product_interested`
2. **Exclude DNC Lists**: Always exclude `DNC` (Do Not Contact) and `unsubscribed` labels
3. **Test with Small Groups**: Test campaigns with a small subset before sending to large audiences
4. **Segment by Engagement**: Use labels to track engagement levels and target accordingly
5. **WhatsApp Opt-ins**: Ensure contacts have explicitly opted-in to receive WhatsApp messages

### Message Content

1. **Follow WhatsApp Policies**: Adhere to WhatsApp Business Platform messaging policies
2. **Use Approved Templates**: For certain message types, use pre-approved message templates
3. **Personalization**: Leverage contact fields for personalized messaging
4. **Rich Media**: Utilize images, videos, and documents to enhance engagement
5. **Clear CTAs**: Include clear call-to-action with trackable links
6. **Timing**: Consider time zones and send during appropriate hours for your audience

### Campaign Management

1. **Monitor Delivery**: Check campaign logs regularly for delivery issues
2. **Track Performance**: Monitor read rates, reply rates, and conversions
3. **Handle Failures**: Review failed messages and update contact information
4. **Respect Opt-outs**: Process unsubscribe requests immediately
5. **Link Shortening**: Enable link shortening for better tracking and analytics
6. **Compliance**: Ensure compliance with local messaging regulations and WhatsApp policies

### WhatsApp-Specific Best Practices

1. **Business Verification**: Ensure your WhatsApp Business account is properly verified
2. **Template Management**: Manage and update message templates regularly
3. **Media Quality**: Use high-quality media files that comply with WhatsApp's size limits
4. **Response Time**: Be prepared to handle replies promptly as WhatsApp users expect quick responses
5. **Conversation Context**: Maintain conversation context when sending follow-up messages

## Conclusion

Utilizing the SeaX API for WhatsApp Business Platform Campaigns enables efficient and dynamic interaction with your audience. Proper setup, continuous monitoring, and adherence to best practices will enhance your campaign's effectiveness and outreach.
