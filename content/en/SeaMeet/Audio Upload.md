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

You can also access the Swagger API docs [here](./Docs/audio-upload-api/)

## Endpoint
`POST https://meet.seasalt.ai/seameet-api/api/v1/workspaces/{workspace_id}/create_meeting_by_audio`

## Allowed Fields in Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Meeting display name |
| `start_time` | string | ✅ | start time of the meeting (e.g. `2020-06-09 10:25:47.116777`) |
| `language` | string | ✅ | BCP-47 language code (e.g. en-US, zh-TW) |
| `folder_path` | string | ✖️ | Storage path for audio file (S3/EFS) |
| `file_name` | string | ✖️ | Audio filename with extension |
| `diarization_options` | string | ✖️ | Speaker separation method (`disabled`, `by_server`) |
| `num_speakers` | integer | ✖️ | Number of speakers in the audio |
| `audio_sample_rate` | integer | ✖️ | Audio sample rate (e.g. 16000) |
| `scenario` | string | ✖️ | Processing scenario (e.g. `customer_service_call`) |
| `scenario_parameters` | object | ✖️ | Advanced scenario configuration |
| → `went_to_voicemail` | boolean | ✖️ | Whether the call reached voicemail |
| → `contains_recordings` | boolean | ✖️ | Presence of recorded messages |
| → `spoke_to_agent` | boolean | ✖️ | Successful agent connection |
| → `customer_number` | string | ✖️ | Customer phone number in E.164 format |
| → `customer_name` | string | ✖️ | Customer identifier/name |
| → `agent_name` | string | ✖️ | Handling agent's name |
| → `direction` | string | ✖️ | Call direction (INBOUND/OUTBOUND) |
| → `enable_agent_recognition` | boolean | ✖️ | Enable voiceprint detection |

## Sample Request
```bash
curl -X POST "https://meet.seasalt.ai/seameet-api/api/v1/workspaces/{workspace_id}/create_meeting_by_audio" \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test title",
    "start_time": "2020-06-09 10:25:47.116777",
    "scenario": "customer_service_call",
    "scenario_parameters": {
      "went_to_voicemail": false,
      "contains_recordings": false,
      "spoke_to_agent": false,
      "customer_number": "+886933123456",
      "customer_name": "test_customer",
      "agent_name": "test_agent",
      "direction": "INBOUND",
      "enable_agent_recognition": true
    },
    "folder_path": "",
    "file_name": "",
    "speaker_accounts": [
      "speaker1",
      "speaker2"
    ],
    "diarization_options": "by_server",
    "num_speakers": 2,
    "enable_itn": true,
    "enable_punctuation": true,
    "language": "en-US",
    "audio_sample_rate": 8000
  }'
