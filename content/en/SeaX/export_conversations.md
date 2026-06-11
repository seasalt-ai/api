---
title: Export Conversations
linkTitle: Export Conversations
description:
  Export a channel's conversation history to a ZIP of per-conversation CSV files
  using the SeaX API, then poll the export job for a 24-hour download link.
categories: [API, Conversations, Export]
tags: [conversations, export, csv, zip, download]
type: docs
weight: 9
---

## Overview

This guide shows how to export the conversations of a single channel over a date
range. The export is **asynchronous**:

- You trigger an export and immediately receive an `export_job_id`.
- The job runs in the background, writing **one CSV per conversation** and
  bundling them into a single **ZIP** file.
- You poll the job until it finishes to obtain a **presigned download URL**
  (valid for 24 hours). If you provide a notification email, the link is also
  emailed to that address.

This guide covers:

- Triggering a conversation export for a channel and date range
- Identifying the channel by `channel_id` or by `phone_number`
- Polling the export job and downloading the ZIP
- The structure of the exported ZIP and CSV files

## Authorization: API Key

Ensure the following are in place:

### **1\. Generate Your API Key**

All APIs require a valid API key issued from your workspace. All requests must
include a valid API key in the request header (`X-API-Key`).

- Go to **Workspace → API Key** tab.

- Click **Add New Key** and check `Workspace Events Notification` as the scope.

- Copy the key and keep it safe. This key is required in the `X-API-Key` header
  for **all requests**.

## How It Works

1. **Trigger** the export with `POST .../export-conversations`. The response
   returns an `export_job_id` with status `queued`.
2. **Poll** the job with `GET .../export-conversations/{export_job_id}` until
   `status` is `finished`.
3. **Download** the ZIP from the `presigned_url` in the status response. The URL
   expires 24 hours after the job finishes.

## API Specification

### 1) Trigger a Conversation Export

`POST /api/v1/workspace/{workspace_id}/export-conversations`

Enqueue an export job for one channel over an inclusive date range. The channel
can be identified either by its `channel_id` (the phone/channel UUID) or by its
`phone_number` in E.164 format.

Path / Header

| Field          | Type              | Description               | Allowed Values / Example               | Required |
| -------------- | ----------------- | ------------------------- | -------------------------------------- | -------- |
| `X-API-Key`    | `string (header)` | Authorization with APIKey | `<your_api_key>`                       | ✅       |
| `workspace_id` | `string (path)`   | Workspace ID              | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |

Request Body: ExportConversationsRequest

| Field                | Type     | Description                                                                                                                 | Allowed Values / Example                 | Required |
| -------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------- |
| `start_date`         | `string` | Start of the range (inclusive), `YYYY-MM-DD`. Cannot be in the future.                                                      | `"2026-02-01"`                           | ✅       |
| `end_date`           | `string` | End of the range (inclusive), `YYYY-MM-DD`. Must be on or after `start_date`.                                               | `"2026-02-28"`                           | ✅       |
| `channel_id`         | `string` | Channel/phone UUID. Provide either `channel_id` **or** `phone_number`.                                                       | `"a1b2c3d4-1111-2222-3333-444455556666"` |          |
| `phone_number`       | `string` | Channel phone number in E.164 format. Used to look up the channel in the workspace.                                         | `"+12025550123"`                         |          |
| `channel_type`       | `string` | Disambiguates a phone number shared by multiple channels (e.g. a WhatsApp and an SMS channel on the same number).           | `sms`, `whatsapp`, `messenger`, `instagram`, `line` |          |
| `notification_email` | `string` | Email address to send the download link to when the export is ready.                                                        | `"agent@example.com"`                    |          |

**Choosing the channel**

Identify the channel with **either** `channel_id` **or** `phone_number` —
provide exactly one. If you omit both, the request returns `422` with the
message `either channel_id or phone_number must be provided`.

**When a phone number is shared by several channels**

The same number can belong to more than one channel (for example a WhatsApp
channel and an SMS channel that share a number). In that case `phone_number`
alone is ambiguous and the request returns `409` with a `candidates` list. Retry
with one of the following:

- `channel_type` — the coarse category of the channel you want. Accepted values:
  `sms`, `whatsapp`, `messenger`, `instagram`, `line`.
- `channel_id` — the exact channel, which is unambiguous on its own.

> The `channel_type` shown for each candidate in the `409` response is the
> channel's detailed internal type (e.g. `LOCAL` or `WHATSAPP_BUSINESS_PLATFORM`),
> which maps to the coarse value you send (`LOCAL` → `sms`,
> `WHATSAPP_BUSINESS_PLATFORM` → `whatsapp`). You always send the coarse value.

**One export at a time**

Only one active export is allowed per channel and date range. Requesting another
while one is still running returns `409`.

###### Example

Request:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/export-conversations' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <your_api_key>' \
  -d '{
    "channel_id": "a1b2c3d4-1111-2222-3333-444455556666",
    "start_date": "2026-02-01",
    "end_date": "2026-02-28",
    "notification_email": "agent@example.com"
  }'
```

Identifying the channel by phone number and type instead:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/export-conversations' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <your_api_key>' \
  -d '{
    "phone_number": "+12025550123",
    "channel_type": "whatsapp",
    "start_date": "2026-02-01",
    "end_date": "2026-02-28",
    "notification_email": "agent@example.com"
  }'
```

Response (`202 Accepted`):

```json
{
  "export_job_id": "79f13adf-f7dc-4744-8ad9-a16b4913e52c",
  "status": "queued",
  "message": "Export job created. You will be emailed a download link when it is ready."
}
```

#### Error responses

A phone number that matches multiple channels (`409 Conflict`):

```json
{
  "detail": {
    "message": "Multiple channels match this phone number. Specify channel_type or channel_id.",
    "candidates": [
      {
        "channel_id": "a1b2c3d4-1111-2222-3333-444455556666",
        "channel_type": "WHATSAPP_BUSINESS_PLATFORM",
        "name": "WhatsApp Sales"
      },
      {
        "channel_id": "b2c3d4e5-7777-8888-9999-000011112222",
        "channel_type": "LOCAL",
        "name": "SMS Support"
      }
    ]
  }
}
```

| Status | Reason                                                                          |
| ------ | ------------------------------------------------------------------------------- |
| `400`  | `start_date` is in the future.                                                  |
| `401`  | Missing or invalid `X-API-Key`.                                                 |
| `404`  | No channel found for the given `channel_id`, or no channel for the phone number. |
| `409`  | The phone number matches multiple channels, or an export for this channel/date range is already in progress. |
| `422`  | Request body validation failed — e.g. neither `channel_id` nor `phone_number` provided, an invalid date format, `end_date` before `start_date`, or an invalid `phone_number` / `channel_type`. |

### 2) Get Export Job Status

`GET /api/v1/workspace/{workspace_id}/export-conversations/{export_job_id}`

Poll an export job. While the job is running, `status` is `queued` or `started`
and `presigned_url` is `null`. When the job is `finished`, `presigned_url`
contains a download link valid for 24 hours. If the job `status` is `failed`,
`presigned_url` stays `null` and `error_message` contains the failure detail.

Path / Header

| Field           | Type              | Description               | Allowed Values / Example               | Required |
| --------------- | ----------------- | ------------------------- | -------------------------------------- | -------- |
| `X-API-Key`     | `string (header)` | Authorization with APIKey | `<your_api_key>`                       | ✅       |
| `workspace_id`  | `string (path)`   | Workspace ID              | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `export_job_id` | `string (path)`   | The job ID returned by the trigger endpoint | `79f13adf-f7dc-4744-8ad9-a16b4913e52c` | ✅       |

Response fields

| Field                       | Type             | Description                                                                |
| --------------------------- | ---------------- | -------------------------------------------------------------------------- |
| `export_job_id`             | `string`         | The export job ID.                                                         |
| `workspace_id`              | `string`         | Workspace ID.                                                              |
| `channel_id`                | `string`         | The channel/phone UUID that was exported.                                  |
| `start_date`                | `string`         | Start of the exported range (`YYYY-MM-DD`).                                |
| `end_date`                  | `string`         | End of the exported range (`YYYY-MM-DD`).                                  |
| `status`                    | `string`         | `queued`, `started`, `finished`, or `failed`.                              |
| `presigned_url`             | `string \| null` | Download URL for the ZIP, available when `status` is `finished`.           |
| `presigned_url_expires_at`  | `string \| null` | When the download URL expires (24 hours after completion).                 |
| `error_message`             | `string \| null` | Failure detail when `status` is `failed`.                                  |
| `created_time`              | `string`         | When the export job was created.                                           |

###### Example

Request:

```bash
curl -X 'GET' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/3fa85f64-5717-4562-b3fc-2c963f66afa6/export-conversations/79f13adf-f7dc-4744-8ad9-a16b4913e52c' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response (still running):

```json
{
  "export_job_id": "79f13adf-f7dc-4744-8ad9-a16b4913e52c",
  "workspace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "channel_id": "b2c3d4e5-7777-8888-9999-000011112222",
  "start_date": "2026-06-01",
  "end_date": "2026-06-10",
  "status": "started",
  "presigned_url": null,
  "presigned_url_expires_at": null,
  "error_message": null,
  "created_time": "2026-06-11T06:50:43.861185"
}
```

Response (finished):

```json
{
  "export_job_id": "79f13adf-f7dc-4744-8ad9-a16b4913e52c",
  "workspace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "channel_id": "b2c3d4e5-7777-8888-9999-000011112222",
  "start_date": "2026-06-01",
  "end_date": "2026-06-10",
  "status": "finished",
  "presigned_url": "https://seax-bulksms.s3.amazonaws.com/conversation_exports/.../SMS_Support_2026-06_1c4639da.zip?AWSAccessKeyId=...&Signature=...&Expires=...",
  "presigned_url_expires_at": "2026-06-12T06:50:47.847864",
  "error_message": null,
  "created_time": "2026-06-11T06:50:43.861185"
}
```

Download the ZIP from `presigned_url`:

```bash
curl -o conversations.zip 'https://seax-bulksms.s3.amazonaws.com/conversation_exports/.../SMS_Support_2026-06_1c4639da.zip?...'
```

## Export File Format

The export is a ZIP archive containing one CSV file per conversation.

**ZIP file name:** `<channel>_<YYYY-MM>_<id>.zip` — for example
`SMS_Support_2026-06_1c4639da.zip`, where `<channel>` is the channel name (or
phone number), `<YYYY-MM>` is taken from the start date, and `<id>` is a short
unique suffix.

**CSV file name (per conversation):** `<contact>--<created_at>--<channel>.csv` —
for example `Jane Doe--2026-04-08_032443--SMS Support (+12025550123).csv`.

**CSV columns:**

| Column            | Description                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------- |
| `message_id`      | Unique message ID.                                                                                      |
| `conversation_id` | ID of the conversation this message belongs to.                                                         |
| `contact_name`    | The contact's name.                                                                                     |
| `contact_phone`   | The contact's phone number.                                                                             |
| `direction`       | `inbound` (from the contact) or `outbound` (from the channel).                                           |
| `speaker_type`    | Who sent the message: `bot`, `agent`, or `customer`.                                                    |
| `speaker_name`    | Full name of the speaker — the bot name, the agent's full name, or the contact's name respectively.     |
| `message_time`    | ISO 8601 timestamp of the message.                                                                      |
| `message_text`    | The message body.                                                                                       |
| `media_url`       | Comma-separated media URLs attached to the message, if any.                                             |
| `status`          | Delivery status of the message.                                                                         |
| `sender_account`  | The account of the sending agent, if the message was sent by a human agent.                             |
