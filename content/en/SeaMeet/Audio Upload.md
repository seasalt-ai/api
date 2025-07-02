---
title: Audio Upload
linkTitle: Audio Upload API Tutorial
description: API endpoint for creating meetings from audio recordings
categories: [API, Audio Processing]
tags: [meeting, audio, diarization]
type: docs
weight: 30
---

## Overview
Create a new meeting by analyzing audio recordings. This endpoint handles audio uploads, initiates processing, and returns a job ID for tracking analysis progress.

You can also access the RESTful API docs of Event Webhooks [here](./Docs/audio-upload-api/)

## Endpoint
`POST https://meet.seasalt.ai/seameet-api/api/v1/workspaces/{workspace_id}/create_meeting_by_audio`

## Allowed Fields in Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Meeting display name |
| `folder_path` | string | ✅ | Storage path for audio file (S3/EFS) |
| `file_name` | string | ✅ | Audio filename with extension |
| `diarization_options` | string | ✅ | Speaker separation method (`disabled`, `by_server`) |
| `language` | string | ✅ | BCP-47 language code (e.g. en-US, zh-TW) |
| `scenario` | string | ✖️ | Processing scenario (e.g. `customer_service_call`) |
| `enable_itn` | boolean | ✖️ | Enable inverse text normalization (default: true) |
| `enable_punctuation` | boolean | ✖️ | Enable automatic punctuation (default: true) |

## Sample Request
```javascript
curl -X POST "https://meet.seasalt.ai/seameet-api/api/v1/workspaces/{workspace_id}/create_meeting_by_audio" \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Client Call Analysis",
    "folder_path": "/recordings/2024-Q2",
    "file_name": "client_call_20240515.wav",
    "diarization_options": "by_server",
    "language": "en-US",
    "scenario_parameters": {
      "customer_number": "+886912345678",
      "agent_name": "John Doe"
    }
  }'