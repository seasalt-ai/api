---
title: Get Meeting Labels
linkTitle: Meeting Labels
description:
  Learn how to retrieve meeting labels by meeting ID or time range using the
  SeaMeet API.
type: docs
weight: 8
---

## Overview

This guide shows how to:

- Retrieve meeting labels by a specific meeting ID.
- Retrieve meeting labels within a specific time range.

## Authorization: API Key

Ensure the following are in place:

### 1. Generate Your API Key

All APIs require a valid API key issued from your workspace. All requests must
include a valid API key in the request header (`X-API-Key`). Currently the only UI to get an API key is through [SeaX](https://seax.seasalt.ai).

- Go to **Workspace → API Key** tab.

- Click **Add New Key** and check `seameet` as the scope.

- Copy the key and keep it safe. This key is required in the `X-API-Key` header
  for **all requests**.

## API Specification

### 1. Get Meeting Labels

`GET /api/v1/public/meeting/{workspace_id}/meeting_labels`

Get meeting labels by `meeting_id` or time range. Requires an API key with the seameet scope.

> **Note:** You must provide either `meeting_id` or both `start_time` and `end_time`.

| Field          | Type              | Description                                                                      | Allowed Values / Example               | Required |
| -------------- | ----------------- | -------------------------------------------------------------------------------- | -------------------------------------- | -------- |
| `X-API-Key`    | `string (header)` | API key for authorization (see Authorization)                                    | `<your_api_key>`                       | ✅       |
| `workspace_id` | `string (path)`   | Workspace ID                                                                     | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `meeting_id`   | `string (query)`  | Optional, specific meeting ID                                                    | `2b342a6e177d4b139638bc16bd312291`     |          |
| `start_time`   | `string (query)`  | Optional, start time of the range                                                | `2023-01-01T00:00:00`                  |          |
| `end_time`     | `string (query)`  | Optional, end time of the range                                                  | `2023-01-31T23:59:59`                  |          |
| `timezone`     | `string (query)`  | Optional, timezone for the time range (default: `UTC`)                           | `Asia/Taipei`                          |          |
| `offset`       | `integer (query)` | Optional, determine the number of rows need be skipped (default: 0)              | `0`                                    |          |
| `limit`        | `integer (query)` | Optional, limit the number of returned meetings (default: 50, min: 1, max: 1000) | `50`                                   |          |

###### Example

Request by `meeting_id`:

```bash
curl -X 'GET' \
  'https://seameet.seasalt.ai/api/v1/public/meeting/3fa85f64-5717-4562-b3fc-2c963f66afa6/meeting_labels?meeting_id=2b342a6e177d4b139638bc16bd312291' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Request by time range:

```bash
curl -X 'GET' \
  'https://seameet.seasalt.ai/api/v1/public/meeting/3fa85f64-5717-4562-b3fc-2c963f66afa6/meeting_labels?start_time=2023-01-01T00:00:00&end_time=2023-01-31T23:59:59&timezone=Asia/Taipei&offset=0&limit=50' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <your_api_key>'
```

Response:

```json
{
  "data": [
    {
      "meeting_id": "2b342a6e177d4b139638bc16bd312291",
      "labels": [
        {
          "id": "11111111-2222-4444-3333-555555555555",
          "name": "Weekly Meeting",
          "color": "#19b9c3"
        }
      ]
    }
  ],
  "total": 1
}
```
