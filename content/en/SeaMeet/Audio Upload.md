---
title: Audio Upload
linkTitle: Audio Upload Tutorial
description: API endpoint for creating meetings from audio recordings
categories: [API, Audio Processing]
tags: [meeting, audio, diarization]
type: docs
weight: 30
---

## Overview
Create a new meeting by analyzing audio recordings. This endpoint handles audio uploads, initiates processing, and returns a job ID for tracking analysis progress.

You can also access the Swagger API docs [here](./Docs/audio-upload-api/)

## Quick Start

### Step 0: Authentication
Make sure you have completed prerequisites [here]({{< relref "SeaMeet/_index.md#Prerequisites" >}})

### Step 1: Prepare Audio File
Prepare the audio to be uploaded. Not the following limitations:
#### Supported Languages
| Language Code | Language |
|---------------|-------------|
| `da-DK` | Danish (Denmark) |
| `de-DE` | German (Germany) |
| `en-GB` | English (United Kingdom) |
| `en-IN` | English (India) |
| `en-US` | English (United States) |
| `es-ES` | Spanish (Spain) |
| `es-MX` | Spanish (Mexico) |
| `fi-FI` | Finnish (Finland) |
| `fr-FR` | French (France) |
| `he-IL` | Hebrew (Israel) |
| `hi-IN` | Hindi (India) |
| `id-ID` | Indonesian (Indonesia) |
| `it-IT` | Italian (Italy) |
| `ja-JP` | Japanese (Japan) |
| `ko-KR` | Korean (South Korea) |
| `pl-PL` | Polish (Poland) |
| `pt-BR` | Portuguese (Brazil) |
| `pt-PT` | Portuguese (Portugal) |
| `sv-SE` | Swedish (Sweden) |
| `zh-CN` | Chinese (China) |
| `zh-TW` | Chinese (Taiwan) |
#### Supported formats
MP3, WAV/PCM, WAV/ALAW, WAV/MULAW, MP3, OGG/OPUS, FLAC, WMA, AAC, AMR, WebM, SPEEX.
#### Audio duration
Maximum of 2 hours.

### Step 2: Upload Audio
Upload the audio file to the API endpoint.

### Step 3: Check Meeting in SeaMeet
Navigate to the `File List` tab from the left sidebar to verify the results of the uploaded audio file.

![seameet file list](/images/seameet-file-list.png)

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
| `scenario_parameters` | object | ✖️ | Advanced scenario configurations, see [more](#advanced-configuration-scenario_parameters) |

### Advanced configuration (`scenario_parameters`)
#### `customer_service_call`
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `went_to_voicemail` | boolean | ✖️ | Whether the call reached voicemail |
| `contains_recordings` | boolean | ✖️ | Presence of recorded messages |
| `spoke_to_agent` | boolean | ✖️ | Successful agent connection |
| `customer_number` | string | ✖️ | Customer phone number in E.164 format |
| `customer_name` | string | ✖️ | Customer identifier/name |
| `agent_name` | string | ✖️ | Agent's identifier/name |
| `direction` | string | ✖️ | Call direction (`INBOUND`/`OUTBOUND`) |
| `enable_agent_recognition` | boolean | ✖️ | Enable AI detection of which speaker is the agent based on conversation |


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
