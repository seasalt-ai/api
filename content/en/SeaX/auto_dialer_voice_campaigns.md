---
title: Auto-Dialer Voice Campaigns
linkTitle: Auto-Dialer Voice Campaigns
description: API endpoints for configuring and initiating bulk outbound voice call campaigns with AI agents.
categories: [API, Auto-Dialer Campaign, AI Agent Campaign, Voice Campaigns]
tags: [auto dialer, voice calls, ai agent, campaign, bulk calls]
type: docs
weight: 30
---

# Auto-Dialer Voice Campaigns

## Overview

The Auto-Dialer Voice Campaigns endpoint enables automated placement of bulk outbound voice calls to selected contact lists, supporting both AI-powered conversational agents and pre-recorded voice drops. Through a structured configuration interface, users can define campaign parameters such as target groups, call scripts, scheduling windows, and fallback behaviors. The endpoint facilitates scalable voice outreach by handling call queuing, delivery tracking, and engagement logging. Each campaign instance generates detailed execution metrics and outcomes, enabling real-time monitoring and performance analysis. Secure access to campaign operations requires authentication via API key. Below we will cover the endpoints needed to customize, create, and monitor your own voice call campaigns. Note: in this tutorial we are assuming you have configured a phone number, contacts, and AI agents in your workspace.

After reading through this tutorial, try out the endpoints [here](./Docs/bulk-sms-api/)

## Getting Started

### Authorization

You must provide your API key in the `X-API-KEY` header.

To set up your API Key

- Go to **Account → API Key** tab.
- Refresh the Key if needed
- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

### Get Phone Numbers

`GET /api/v1/workspace/{workspace_id}/phones`

First you must find the available phone numbers. You will need to collect the `id` of each number you would like to run the campaign from.

| Field           | Type               | Description                                                                                                      | Allowed Values / Example                                                   | Required |
|-----------------|--------------------|------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------|
| `X-API-Key`     | `string (header)`   | API key for authorization. Required in header. See [Authorization Guide](#authorization) | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`                                                           | ✅        |
| `workspace_id`  | `string (path)`     | Unique identifier of the workspace                                                                               | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                        | ✅        |
| `offset`        | `integer (query)`   | Number of results to skip before starting to return.<br>Minimum: 0<br>Default: 0                                 | `0`                                                                         |          |
| `limit`         | `integer (query)`   | Max number of results to return after skipped offset. If 0, return all.<br>Minimum: 0<br>Default: 10             | `10`                                                                        |          |
| `is_owned`      | `boolean (query)`   | Filter for owned records only.<br>Default: `false`                                                               | `true`, `false`                                                             |          |
| `enabled`       | `boolean (query)`   | Filter by whether the item is enabled.<br>Default: `true`                                                        | `true`, `false`                                                             |          |
| `voice_available` | `boolean (query)` | Filter by voice capability availability                                                                          | `true`, `false`                                                             |          |

###### Example

Request:
```
curl -X 'GET' \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/phones?offset=0&limit=10&is_owned=false&enabled=true&voice_available=true' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28'
```

Response:
```
{
  "data": [
    {
      "name": "tech support",
      "enabled": true,
      "phone": "+886912123456",
      "country": "US",
      "whatsapp_device_id": "1234567890:98@s.whatsapp.net",
      "whatsapp_status": "CONNECTING",
      "generic_reply_message": "Welcome! If you want to subscribe daily report, please reply 'DAILY'.",
      "dnc_reply_message": "Ok, we won't send you any other message.",
      "enabled_generic_reply": false,
      "enabled_dnc_reply": false,
      "type": "LOCAL",
      "source": "TWILIO",
      "phone_capability": {
        "sms": false,
        "mms": false,
        "voice": false,
        "fax": false,
        "whatsapp": false,
        "whatsapp_business_platform": false
      },
      "is_default": false,
      "enabled_recipient": false,
      "whatsapp_business_account_phone_id": "555555555555",
      "dialpad_available": false,
      "created_time": "2025-07-07T18:12:58.351633",
      "updated_time": "2025-07-07T18:12:58.351649",
      "id": "0354fb10-9e18-4923-a213-6253800f8d01",
      "call_recipient": {
        "id": "0354fb10-9e18-4923-a213-6253800f8d01",
        "type": "PHONE_NUMBER",
        "receiver": "+1234567890"
      },
      "sms_recipient": {
        "id": "0354fb10-9e18-4923-a213-6253800f8d01",
        "type": "PHONE_NUMBER",
        "receiver": "+1234567890"
      },
      "wabp_recipient": {
        "id": "0354fb10-9e18-4923-a213-6253800f8d01",
        "type": "PHONE_NUMBER",
        "receiver": "+1234567890"
      },
      "verified_caller": {
        "created_time": "2025-07-07T18:12:58.351633",
        "updated_time": "2025-07-07T18:12:58.351649",
        "id": "0354fb10-9e18-4923-a213-6253800f8d01",
        "phone_number": "+1234567890",
        "name": "+1234567890",
        "validation_code": "813955",
        "status": "failed",
        "call_id": "CAca1ce90f90c7609477eee1f6bbc75a50"
      },
      "byoc_trunk": {
        "created_time": "2025-07-07T18:12:58.351633",
        "updated_time": "2025-07-07T18:12:58.351649",
        "id": "0354fb10-9e18-4923-a213-6253800f8d01",
        "sip_domain": "string",
        "acl_ip_addresses": [
          {
            "ip_address": "string",
            "port": 0,
            "id": "0354fb10-9e18-4923-a213-6253800f8d01"
          }
        ],
        "sip_auth_username": "string",
        "sip_auth_password": "string"
      },
      "users": [
        {
          "account": "satoshi",
          "first_name": "Satoshi",
          "last_name": "Nakamoto",
          "email": "satoshi@btc.com",
          "phone": "+1230000000",
          "language": "en-US",
          "theme": "dark",
          "date_format": "MM/dd/yyyy",
          "time_format": "HH:mm:ss",
          "created_time": "2009-01-03T18:15:00",
          "email_notification_enabled": false,
          "is_new_user": false,
          "email_notification_only_offline": false,
          "sms_notification_enabled": false,
          "sms_notification_only_offline": false
        }
      ],
      "keywords": [
        {
          "name": "want",
          "reply": "OK, we got it.",
          "enabled_auto_reply": true,
          "enabled_contact_label": true,
          "keep_dnc_label_only": false,
          "id": "11111111-2222-4444-3333-555555555555",
          "phone_id": "11111111-2222-4444-3333-555555555555",
          "priority": 10,
          "contact_labels": [
            {
              "name": "test",
              "color": "#19b9c3",
              "description": "This label is for vip customer",
              "id": "11111111-2222-4444-3333-555555555555",
              "is_system": true,
              "created_time": "2025-07-07T18:13:02.656081",
              "updated_time": "2025-07-07T18:13:02.656093"
            }
          ],
          "created_time": "2025-07-07T18:13:02.665302",
          "updated_time": "2025-07-07T18:13:02.665315"
        }
      ],
      "unread_count": 0
    }
  ],
  "total": 0
}
```

### Get Contacts

`GET /api/v1/workspace/{workspace_id}/contacts`

Use this endpoint to retrieve the set of contacts you’d like to call during the campaign.

| Field                          | Type               | Description                                                                                                                     | Allowed Values / Example                                                                                             | Required |
|-------------------------------|--------------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|----------|
| `X-API-Key`    | `string (header)`   | Authorization with API key. See [Authorization Guide](#authorization)  | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`                                                   | ✅        |
| `workspace_id`  | `string (path)`     | Unique identifier of the workspace                                                                               | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                        | ✅        |
| `offset`                      | `integer (query)`   | Number of rows to skip.<br>Minimum: 0<br>Default: `0`                                                                            | `0`                                                                                                                    |          |
| `limit`                       | `integer (query)`   | Number of rows to return after skipped offset. If 0, return all.<br>Minimum: 0<br>Default: `10`                                 | `10`                                                                                                                   |          |
| `keyword`                     | `string (query)`    | Optional search keyword for contact names and phones.<br>Default: *empty*                                                       | `+18111222333`                                                                                                        |          |
| `whatsapp_phone`             | `string (query)`    | Optional search for contacts by WhatsApp phone.<br>Default: *empty*                                                             | `+18111222333`                                                                                                        |          |
| `all_contact_label_ids`       | `string (query)`    | Search contacts that must match **all** specified label IDs.<br>Comma-separated UUIDs                                           | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666`                                           |          |
| `any_contact_label_ids`       | `string (query)`    | Search contacts that match **any** of the specified label IDs.<br>Comma-separated UUIDs                                         | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666`                                           |          |
| `exclude_contact_ids`         | `string (query)`    | Exclude contacts by contact IDs from the result.<br>Comma-separated UUIDs                                                       | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666`                                           |          |
| `exclude_any_contact_label_ids`| `string (query)`   | Exclude contacts that match **any** of the specified label IDs.<br>Comma-separated UUIDs                                        | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666`                                           |          |
| `exclude_all_contact_label_ids`| `string (query)`   | Exclude contacts that match **all** of the specified label IDs.<br>Comma-separated UUIDs                                        | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666`                                           |          |
| `addition_contact_ids`        | `string (query)`    | Include contacts explicitly by contact IDs, in addition to label-based search.<br>Comma-separated UUIDs                        | `11111111-2222-4444-3333-555555555555,11111111-2222-4444-3333-666666666666`                                           |          |
| `order_by`                    | `string (query)`    | Optional sorting. Comma-separated list of `field:direction` pairs.<br>Default: `created_time:desc`                              | `phone:asc,created_time:desc,name:asc`                                                                               |          |
| `exclude_labels`              | `string (query)`    | Exclude contacts with one or more of these label **names** (not IDs).<br>Comma-separated values                                 | `DNC,invalid number,unreachable`                                                                                      |          |
| `whatsapp_phone_only` | `boolean (query)`   | If true, filters to only return contacts with a WhatsApp phone number.<br>Default: `false` | `true`, `false` |

###### Example

Request:
```
curl -X 'GET' \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/contacts?offset=0&limit=10&keyword=%2B18111222333&whatsapp_phone=%2B18111222333&all_contact_label_ids=11111111-2222-4444-3333-555555555555%2C11111111-2222-4444-3333-666666666666&any_contact_label_ids=11111111-2222-4444-3333-555555555555%2C11111111-2222-4444-3333-666666666666&exclude_contact_ids=11111111-2222-4444-3333-555555555555%2C11111111-2222-4444-3333-666666666666&exclude_any_contact_label_ids=11111111-2222-4444-3333-555555555555%2C11111111-2222-4444-3333-666666666666&exclude_all_contact_label_ids=11111111-2222-4444-3333-555555555555%2C11111111-2222-4444-3333-666666666666&addition_contact_ids=11111111-2222-4444-3333-555555555555%2C11111111-2222-4444-3333-666666666666&order_by=phone%3Aasc%2Ccreated_time%3Adesc%2Cname%3Aasc&exclude_labels=DNC%2Cinvalid%20number%2Cunreachable&whatsapp_phone_only=false' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28'
```

Response:
```
{
  "data": [
    {
      "name": "Test1",
      "phone": "+12345678900",
      "note": "New contact",
      "whatsapp_phone": "+12345678900",
      "contact_field_data": {
        "field1": 1
      },
      "id": "11111111-2222-4444-3333-555555555555",
      "workspace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "created_time": "2025-07-07T18:13:04.845276",
      "updated_time": "2025-07-07T18:13:04.845287",
      "contact_labels": [
        {
          "name": "test",
          "color": "#19b9c3",
          "description": "This label is for vip customer",
          "id": "11111111-2222-4444-3333-555555555555",
          "is_system": true,
          "created_time": "2025-07-07T18:13:02.656081",
          "updated_time": "2025-07-07T18:13:02.656093"
        }
      ]
    }
  ],
  "total": 0
}
```

### Get Configured AI agents

GET /api/v1/workspace/{workspace_id}/ai_agents

Use this endpoint to get a list of available ai agents to use during the call. You’ll need the `conversation_config_id` in order to select a particular agent for the campaign creation.


| Field        | Type               | Description                                                                                                     | Allowed Values / Example                                             | Required |
|--------------|--------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|----------|
| `X-API-Key`    | `string (header)`   | Authorization with API key.  See [Authorization Guide](#authorization) | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`                                                   | ✅        |
| `workspace_id` | `string (path)`     | Unique identifier of the workspace                                                                             | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                                   | ✅        |
| `types`        | `string (query)`    | Optional filter for AI agent integration types (comma-separated).                                              | `SEAX_CALL`, `SEAX_SMS`, `SEAX_WABP`                                 |          |
| `limit`        | `integer (query)`   | Optional. Number of rows to return after offset. `0` returns all.                                              | Default: `10` <br> Example: `10`                                     |          |
| `offset`       | `integer (query)`   | Optional. Number of rows to skip before returning results.                                                     | Default: `0` <br> Example: `0`                                       |          |
| `order_by`     | `string (query)`    | Optional. Order items by ascending/descending fields (`:` separated, comma-delimited list).                    | Default: `created_time:desc` <br> Example: `created_time:desc`       |          |

###### Example

Request:
```
curl -X 'GET' \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/ai_agents?limit=10&offset=0&order_by=created_time%3Adesc' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28'
```

Response:
```
{
  "data": [
    {
      "id": "0354fb10-9e18-4923-a213-6253800f8d01",
      "name": "",
      "conversation_config_id": "0354fb10-9e18-4923-a213-6253800f8d01",
      "integrations": [
        {
          "inbound_pick_up_message": "Hello, how can I help you?",
          "outbound_starting_message": "Hello, how can I help you?",
          "outbound_voice": "en-US-SteffanNeural",
          "outbound_language": "string",
          "inbound_voice": "en-US-SteffanNeural",
          "inbound_language": "string",
          "type": "SEAX_CALL"
        }
      ]
    }
  ],
  "total": 1
}
```

## Campaign Management

### Create Campaign

#### Initiate Auto-Dialer Voice Campaign

1. POST /api/v1/workspace/{workspace_id}/auto_dialer_campaigns

Use this endpoint to trigger an outbound auto dialer voice campaign.

| Field                          | Type                  | Description                                                                 | Allowed Values / Example                                                   | Required |
|--------------------------------|-----------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|----------|
| `X-API-Key`    | `string (header)`   | Authorization with API key.  See [Authorization Guide](#authorization) | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`                                                   | ✅        |
| `name`                         | `string`              | Campaign name                                                               | `Test`                                                                       | ✅        |
| `phone_ids`                    | `array[string]`       | Phone ID(s) to use for the campaign                                         | `["020086f5-fb0e-4a0c-920a-bbdd04f4381c"]`                                   | ✅        |
| `attach_contact_label_ids`     | `array[string]`       | Labels to attach to contacts after campaign                                 | `[]`                                                                         |          |
| `start_time`                   | `string ($date-time)` | Campaign start timestamp                                                    | `2025-07-08T03:06:09+00:00`                                                  | ✅        |
| `end_time`                     | `string ($date-time)` | Campaign end timestamp                                                      | `2025-07-08T03:15:00+00:00`                                                  | ✅        |
| `is_schedule`                  | `boolean`             | Whether the campaign is scheduled                                           | `false`                                                                      |          |
| `is_timezone_aware`           | `boolean`             | Whether the schedule is timezone aware                                      | `false`                                                                      |          |
| `mode`                         | `string`              | Campaign execution mode                                                     | `WEB`                                                                        | ✅        |
| `stage`                        | `string`              | Processing stage of the campaign                                            | `INSTANCE`                                                                   | ✅        |
| `message`                      | `string`              | Message to be delivered (used by TTS or AI agent)                           | `Hi, do you have a few minutes to take our survey?`                                                  |          |
| `tts_language`                 | `string`              | TTS language code                                                           | `""` (Recommended to leave as empty string to use the default configured in your workspace)                                                                 |          |
| `tts_voice`                    | `string`              | TTS voice type                                                              | `default`                                                                    |          |
| `audio_url`                    | `string`              | Optional audio URL (if not using TTS)                                       | `""` (Recommended to leave as empty string to use default configured on seachat)                                                              |          |
| `type`                         | `string`              | Campaign type                                                               | `AI_AGENT`                                                                   | ✅        |
| `capture_keypress`             | `boolean`             | Enable DTMF (keypress) capture                                              | `true`                                                                       |          |
| `capture_stt`                  | `boolean`             | Enable speech-to-text (STT) capture                                         | `false`                                                                      |          |
| `ai_agent_conversation_config_id` | `string`           | Conversation config ID used by the AI agent                                 | `221316ae-8a9f-4f39-b7f8-f2e756b80a63`                                                            | ✅        |
| `overwrite_phone_recipient.type`     | `string`         | Type of overwrite (who the AI agent is talking to)                          | `AI_AGENT`                                                                   | ✅        |
| `overwrite_phone_recipient.receiver` | `string`         | Receiver identifier for overwrite                                           | `221316ae-8a9f-4f39-b7f8-f2e756b80a63`                                                            | ✅        |
| `exclude_contact_ids`          | `array[string]`       | Contact IDs to exclude                                                      | `["4667298e-8d5b-468e-8218-6a47925fe5f2","aa145964-6d17-488d-a9be-09a43191f329"]`                                                                         |          |
| `any_contact_label_ids`        | `array[string]`       | Include contacts with any of these labels                                   | `["dd20f7cd-03fb-4c79-9f3e-998372d1bec6"]`                                   |          |

###### Example

Request:
```
curl -X 'POST' \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/ffffffff-abcd-4000-0000-000000000000/auto_dialer_campaigns' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28' \
  -d '{
  "name": "Test",
  "phone_ids": [
    "020086f5-fb0e-4a0c-920a-bbdd04f4381c"
  ],
  "attach_contact_label_ids": [],
  "start_time": "2025-07-08T03:06:09+00:00",
  "is_schedule": false,
  "is_timezone_aware": false,
  "mode": "WEB",
  "stage": "INSTANCE",
  "message": "您好，請問您現在方便講話嗎?",
  "tts_language": "",
  "audio_url": "",
  "type": "AI_AGENT",
  "capture_keypress": true,
  "end_time": "2025-07-08T03:15:00+00:00",
  "ai_agent_conversation_config_id": "221316ae-8a9f-4f39-b7f8-f2e756b80a63",
  "overwrite_phone_recipient": {
    "type": "AI_AGENT",
    "receiver": "221316ae-8a9f-4f39-b7f8-f2e756b80a63"
  },
  "exclude_contact_ids": [
      "4667298e-8d5b-468e-8218-6a47925fe5f2",
      "aa145964-6d17-488d-a9be-09a43191f329"
  ],
  "any_contact_label_ids": [
    "dd20f7cd-03fb-4c79-9f3e-998372d1bec6"
  ],
  "tts_voice": "default",
  "capture_stt": false
}'
```

#### `overwrite_phone_recipient`

This parameter is **only required if any of the `phone_ids` have a default recipient that does not match the campaign recipient**. It allows you to explicitly override the default recipient setting for those phone numbers. You must include the `type` (in this example AI_AGENT) and the `receiver` (in this example the conversation config of the ai agent)

##### Format:
```
"overwrite_phone_recipient": {
  "type": "AI_AGENT",
  "receiver": "221316ae-8a9f-4f39-b7f8-f2e756b80a63"
}
```

#### `any_contact_label_ids` and `exclude_contact_ids`
By default, the campaign will call every contact that matches the label ids under `any_contact_label_ids`. To exclude contacts you must include the contact ids in the `exclude_contact_ids` list. 

##### Format:
```
  "exclude_contact_ids": [
      "4667298e-8d5b-468e-8218-6a47925fe5f2",
      "aa145964-6d17-488d-a9be-09a43191f329"
  ],
```
 

### List Campaigns

`GET /api/v1/workspace/{workspace_id}/auto_dialer_campaigns`

Use this endpoint to gather information about past and current campaigns. Filter on various attributes such as campaign type, status, mode, and date range.

Allowed query parameters.

| Field                          | Type                | Description                                                                                      | Allowed Values / Example                                                                                      | Required |
| ----------------------------- | ------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | -------- |
| `X-API-Key`                   | `string (header)`    | API key used for authenticating requests                                                         | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`                                                                                             | ✅       |
| `workspace_id`                | `string (path)`      | Unique identifier of the workspace                                                              | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                                                                                   | ✅       |
| `types`                       | `string (query)`     | Filter by one or more auto dialer campaign types (comma-separated)                              | `VOICE_DROP`, `PROGRESSIVE_DIALER`, `AI_AGENT`                                                                |          |
| `phone_numbers`               | `string (query)`     | Filter by one or more phone numbers (comma-separated)                                            | `+15555550100,+15555550101`                                                                                   |          |
| `ai_agent_conversation_config_id` | `string (query)` | Filter by AI agent conversation config ID | `221316ae-8a9f-4f39-b7f8-f2e756b80a63`| |


###### Example

Request:
```
curl -X 'GET' \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/auto_dialer_campaigns?stage=INSTANCE&limit=10&offset=0&order_by=created_time%3Adesc' \
  -H 'accept: application/json' \
  -H 'X-API-Key: e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28'
```
Response:
```
{
  "data": [
    {
      "start_time": "2025-07-08T03:19:39",
      "end_time": "2025-07-08T03:30:00",
      "name": "test",
      "draft_name": null,
      "type": "AI_AGENT",
      "message": "Hello this is a test",
      "tts_language": "en-US",
      "tts_voice": "en-US-default",
      "ai_agent_id": "51fefba9-c3ee-40e8-a392-8bc14c639719",
      "ai_agent_conversation_config_id": "221316ae-8a9f-4f39-b7f8-f2e756b80a63",
      "max_attempts": 1,
      "max_dialers": 20,
      "capture_keypress": true,
      "capture_stt": false,
      "is_timezone_aware": false,
      "is_schedule": false,
      "contact_file_url": null,
      "timezone": null,
      "campaign_metadata": {
        "all_contact_labels": [],
        "any_contact_labels": [
          {
            "id": "7082ae15-43ae-472f-a83c-ee6462a0af83",
            "name": "test group",
            "color": "#0cb3c3"
          }
        ],
        "exclude_contacts": [
          {
            "id": "6e612221-594d-4c22-a305-ffe193b3c51f",
            "name": "Test User 1",
            "phone": "+11234567890"
          },
          {
            "id": "c0c9965b-1809-45e2-bcb6-1e1484a79abb",
            "name": "Test User 2",
            "phone": "+11234567890"
          },
          {
            "id": "a43b4e5d-edc7-4264-be19-2d39ab99d52e",
            "name": "Test User 3",
            "phone": "+11234567890"
          }
        ],
        "addition_contacts": [],
        "exclude_any_contact_labels": [],
        "exclude_all_contact_labels": [],
        "whatsapp_phone_only": false
      },
      "status": "FINISHED",
      "created_time": "2025-07-08T03:19:40.160564",
      "updated_time": "2025-07-08T03:19:40.160564",
      "id": "448ea794-0368-4604-a56f-f2350229d9e5",
      "mode": "WEB",
      "stage": "INSTANCE",
      "audio": null,
      "phones": [
        {
          "name": "dev-number-1",
          "enabled": true,
          "phone": "+19987654321",
          "country": "US",
          "whatsapp_device_id": null,
          "whatsapp_status": null,
          "generic_reply_message": "Welcome!",
          "dnc_reply_message": "Ok, we won't send you any other message.",
          "enabled_generic_reply": false,
          "enabled_dnc_reply": false,
          "type": "LOCAL",
          "source": "TWILIO",
          "phone_capability": {
            "sms": true,
            "mms": true,
            "voice": true,
            "fax": false,
            "whatsapp": false,
            "whatsapp_business_platform": false
          },
          "is_default": false,
          "enabled_recipient": true,
          "whatsapp_business_account_phone_id": null,
          "dialpad_available": false,
          "created_time": "2024-05-14T12:25:05.892618",
          "updated_time": "2025-07-08T03:19:40.160564",
          "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
          "call_recipient": {
            "id": "dde4ffb2-4c8c-412a-a8cf-33b77843cdb0",
            "type": "AI_AGENT",
            "receiver": "221316ae-8a9f-4f39-b7f8-f2e756b80a63"
          },
          "sms_recipient": null,
          "wabp_recipient": null,
          "verified_caller": null,
          "byoc_trunk": null
        }
      ],
      "statistics": {
        "human": 0,
        "machine": 0,
        "unknown": 0,
        "no_answer": 0,
        "total": 1
      },
      "contact_fields": [],
      "relative_time_config": null
    }
  ]
}
```


### Get Campaign Details

`GET /api/v1/workspace/{workspace_id}/auto_dialer_campaigns/{auto_dialer_campaign_id}`

Get the information of a campaign given the workspace_id and the desired campaign_id

| Field                    | Type             | Description                                                                                          | Allowed Values / Example                                           | Required |
|--------------------------|------------------|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|----------|
| `X-API-Key`              | `string (header)`| Authorization with API key.  See [Authorization Guide](#authorization) | `e91772ccb5e6ce5f932d6417eacd9a1e031b957101cdb68be76d417defa7fd28`                                                  | ✅        |
| `workspace_id`           | `string (path)`  | Unique identifier of the workspace                                                                   | `3fa85f64-5717-4562-b3fc-2c963f66afa6`                                                 | ✅        |
| `auto_dialer_campaign_id`| `string (path)`  | Unique identifier of the auto dialer campaign                                                        | `01e14e9e-ddd8-4e63-bad2-e026d5aa5698`                                                  | ✅        |

###### Example

Request:
```
curl -X 'GET' \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/ffffffff-abcd-4000-0000-000000000000/auto_dialer_campaigns/448ea794-0368-4604-a56f-f2350229d9e5' \
  -H 'accept: application/json' \
  -H 'X-API-Key: 09a318b51673ce2e3b1c03387a7bfc8c2e9aa35f83e6295b4109402a0c65111c'
```

Response:
```
{
  "start_time": "2025-07-08T03:19:39",
  "end_time": "2025-07-08T03:30:00",
  "name": "test",
  "draft_name": null,
  "type": "AI_AGENT",
  "message": "Hello this is a test",
  "tts_language": "en-US",
  "tts_voice": "en-US-default",
  "ai_agent_id": "51fefba9-c3ee-40e8-a392-8bc14c639719",
  "ai_agent_conversation_config_id": "221316ae-8a9f-4f39-b7f8-f2e756b80a63",
  "max_attempts": 1,
  "max_dialers": 20,
  "capture_keypress": true,
  "capture_stt": false,
  "is_timezone_aware": false,
  "is_schedule": false,
  "contact_file_url": null,
  "timezone": null,
  "campaign_metadata": {
    "all_contact_labels": [],
    "any_contact_labels": [
      {
        "id": "7082ae15-43ae-472f-a83c-ee6462a0af83",
        "name": "test group",
        "color": "#0cb3c3"
      }
    ],
    "exclude_contacts": [
      {
        "id": "6e612221-594d-4c22-a305-ffe193b3c51f",
        "name": "Test User 1",
        "phone": "+11234567890"
      },
      {
        "id": "c0c9965b-1809-45e2-bcb6-1e1484a79abb",
        "name": "Test User 2",
        "phone": "+11234567890"
      },
      {
        "id": "a43b4e5d-edc7-4264-be19-2d39ab99d52e",
        "name": "Test User 3",
        "phone": "+11234567890"
      }
    ],
    "addition_contacts": [],
    "exclude_any_contact_labels": [],
    "exclude_all_contact_labels": [],
    "whatsapp_phone_only": false
  },
  "status": "FINISHED",
  "created_time": "2025-07-08T03:19:40.160564",
  "updated_time": "2025-07-08T03:19:40.160564",
  "id": "448ea794-0368-4604-a56f-f2350229d9e5",
  "mode": "WEB",
  "stage": "INSTANCE",
  "audio": null,
  "phones": [
    {
      "name": "dev-number-1",
      "enabled": true,
      "phone": "+19987654321",
      "country": "US",
      "whatsapp_device_id": null,
      "whatsapp_status": null,
      "generic_reply_message": "Welcome!",
      "dnc_reply_message": "Ok, we won't send you any other message.",
      "enabled_generic_reply": false,
      "enabled_dnc_reply": false,
      "type": "LOCAL",
      "source": "TWILIO",
      "phone_capability": {
        "sms": true,
        "mms": true,
        "voice": true,
        "fax": false,
        "whatsapp": false,
        "whatsapp_business_platform": false
      },
      "is_default": false,
      "enabled_recipient": true,
      "whatsapp_business_account_phone_id": null,
      "dialpad_available": false,
      "created_time": "2024-05-14T12:25:05.892618",
      "updated_time": "2025-07-08T03:19:40.160564",
      "id": "020086f5-fb0e-4a0c-920a-bbdd04f4381c",
      "call_recipient": {
        "id": "dde4ffb2-4c8c-412a-a8cf-33b77843cdb0",
        "type": "AI_AGENT",
        "receiver": "221316ae-8a9f-4f39-b7f8-f2e756b80a63"
      },
      "sms_recipient": null,
      "wabp_recipient": null,
      "verified_caller": null,
      "byoc_trunk": null
    }
  ],
  "statistics": {
    "human": 0,
    "machine": 0,
    "unknown": 0,
    "no_answer": 0,
    "total": 1
  },
  "contact_fields": [],
  "relative_time_config": null
}
```
