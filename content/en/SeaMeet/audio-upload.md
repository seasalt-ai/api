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

## Quick Start

### Step 0: Authentication and Set up
1. Make sure you have completed prerequisites [here]({{< relref "SeaMeet/_index.md#Prerequisites" >}})
2. If you would like to receive results via callback, you need to follow steps [here]({{< relref "SeaMeet/audio-upload.md#callback-api" >}})

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
| `zh-CN` | Mandarin (China) |
| `zh-TW` | Mandarin (Taiwan) |

#### Supported formats
wav/pcm, wav/alaw, wav/mulaw, mp3, mp4, ogg/opus, flac, wma, aac, amr, webm, speex.

#### Audio duration
Maximum of 2 hours.

### Step 2: Create Meeting
Create SeaMeet meeting instance. [See API]({{< relref "SeaMeet/audio-upload.md#create-meeting" >}})

### Step 3: Upload Audio
First obtain a presigned s3 url and then upload audio to the provided url. [See API]({{< relref "SeaMeet/audio-upload.md#generate-audio-upload-url" >}})

### Step 4: Run Analysis
1. Start the transcription and analysis job. [See API](#run-analysis)
2. Check analysis job status using the job ID [See API](#get-job-by-id)

### Step 5: Get Results
There are two ways to check the results:
- Receive results via callback, make sure you have followed steps [here](#callback-schema) before submitting the analysis job.
- Check results on [SeaMeet](https://meet.seasalt.ai/)


## Create Meeting

### API

POST /api/v1/workspaces/{workspace_id}/meetings

#### Header

| Name | Value | Description |
| :---- | :---- | :---- |
| accept | application/json |  |
| Authorization | Bearer {access_token} | Bearer token |

#### Request Body

| Name | Type | Description | Example | Required |
| :---- | :---- | :---- | :---- | :---- |
| meeting_name | string | Name of the meeting | `“call_1”` | ✅ |
| channel_type | string | Type of the meeting, must be the same as workspace type for now | `“PHONE”` | ✅ |
| language | string | Language of the meeting, should be in \["en-US", “zh-TW”\] | `“zh-TW”` | ✅ |
| start_time | string | UTC Datetime of when the audio began following the ISO 8601 standard. Make sure this matches the timezone setting in the workspace. | `“2024-05-30T21:53:34”` | ✅ |
| resource_metadata | object | **Optional**. Custom data column. Normally, it would fill customer local call id for data consistency.  | `{"call_id": "123"}` | ✖️ |

#### Response Status 200

Normal response with the created workspace info.

##### Status code: 200

##### Example of the response body

```json
{
  id: "seax_139953cfd9e612d6c7827ccebdd7c50c",
  owner_id: "useraccount",
  name: "Meeting Name",
  participants_number: 0,
  status: "INITIAL",
  start_time: "2022-12-07T10:11:42.520327",
  language: "en-US",
  duration: 0,
  flag: "WAITING",
  channel_type: "PHONE",
}
```

## Delete Meeting

### API

DELETE /api/v1/workspaces/{workspace_id}/meetings/{meeting_id}

#### Header

| Name | Value | Description |
| :---- | :---- | :---- |
| accept | application/json |  |
| Authorization | Bearer {access_token} | Bearer token |

#### Response Status 204

No payload return

## Generate Audio Upload URL

### API

POST /api/v1/workspaces/{workspace_id}/meetings/{meeting_id}/upload_audio_url

#### Header

| Name | Value | Description |
| :---- | :---- | :---- |
| accept | application/json |  |
| Authorization | Bearer {access_token} | Bearer token |

#### Request Body

| Name | Type | Description | Example | Required |
| :---- | :---- | :---- | :---- | :---- |
| name | string | File name, if raise error if conflicts | `"file_name.wav"` | ✅ |

#### Response Status 200

Normal response with the created workspace info.

##### Status code: 200

##### Example of the response body

```json
{
  upload_audio_url: "https://xxxxx",
  expired_time: "2024-05-30T21:53:34" // utc
}
```

##### and then upload file to `upload_audio_url`with curl command

```bash
curl -X PUT -T "/path/to/file" "https://xxxxx"
```

or use the python script below.

```python
import requests

url = 'https://xxxxx'
file_path = '/path/to/file'

with open(file_path, 'rb') as f:
    response = requests.put(url, data=f)

print(response.status_code)  # 200
```

#### Response Status 400

MeetingNotFoundError

##### Status code: 400

## Run Analysis

Upload a file as the knowledge base corpus for the bot

### API

POST /api/v1/workspaces/{workspace_id}/meetings/{meeting_id}/analyze_audio

#### Header

| Name | Value | Description |
| :---- | :---- | :---- |
| accept | application/json |  |
| Authorization | Bearer {access_token} | Bearer token |

#### Request Body

| Name | Type | Description | Example | Required |
| :---- | :---- | :---- | :---- | :---- |
| channels | number | Number of channels for the audio, needs to be `1` or `2` | `1` | ✅ |
| file_name | string | file_name of the uploaded audio | `file_name.wav` | ✖️ |
| audio_start_offset | number | Audio start offset from the start of the meeting. | `10.5` | ✖️ |
| audio_format | string | Audio file format, inferred from path extension if not provided. | `wav` | ✖️ |
| audio_sample_rate | number | Audio file sample rate, inferred from file header if not provided. | `8000` | ✖️ |
| audio_encoding | string | Audio file encoding, inferred from file header if not provided. | `pcm_s16le` | ✖️ |
| scenario | string | Scenario of this audio, e.g. `customer_service_call` | `customer_service_call` | ✖️ |
| scenario_parameters | object | Dictionary containing fields specific to the scenario, see [scenario_parameters for customer_service_call](#scenario_parameters-for-customer_service_call) | `{"went_to_voicemail": false, "spoke_to_agent": true}` | ✖️ |
| speaker_accounts | string | **Optional**. The speaker accounts. | `["kontak_customer_181"]` | ✖️ |
| diarization_options | string | either `by_server` or `disabled`, meaning enable and disable diarization respectively. | `by_server` | ✖️ |

#### scenario_parameters for `customer_service_call` {#scenario_parameters-for-customer_service_call}

| Name | Type | Description | Example | Required |
| :---- | :---- | :---- | :---- | :---- |
| customer_number | string | Customer call number. | `0933123456` | ✅ |
| went_to_voicemail | bool | Whether the call went straight to voicemail without being picked up. | `false` | ✖️ |
| contains_recordings | bool | Whether recordings like voicemail or automated voice messages are present in the audio. | `false` | ✖️ |
| spoke_to_agent | bool | Whether the customer spoke to a live agent. Only applicable for inbound calls. If `true` for inbound calls, `went_to_voicemail` is ignored. | `true` | ✖️ |
| customer_name | string | Customer name. | `John Doe` | ✖️ |
| agent_name | string | Agent name. | `Jane Doe` | ✖️ |

#### Response Status 202

The file was successfully uploaded and the data import process started.

##### Status code: 202

##### Response body

| Name | Type | Description | Example |
| :---- | :---- | :---- | :---- |
| id | string | Job ID for the current job. It can be used to query the execution result or compare it with the data obtained from the callback. | `55c09c56-9f99-4da2-bba4-da4722759e02` |
| type | string | Job type for the current job. It would always be `MEETING_ANALYSIS` for this endpoint. | `MEETING_ANALYSIS` |
| status | string | Indicates the status of the job `QUEUED`, `FINISHED`, `FAILED`, or `STARTED`. The analysis will be sent to callback_url after the status changes to `FINISHED` for a period of time. | `QUEUED` |
| result | null | Stay null value through all status. | `null` |
| error_message | string | null | When an error occurs, it returns error information; otherwise, it is null if no errors occur | `null` |
| `relations` | object | It would contain two keys: “workspace_id”, “meeting_id”. All of the keys have their id.  | `{"meeting_id": "55c09c56-9f99-4da2-bba4-da4722759e01", "workspace_id": "55c09c56-9f99-4da2-bba4-da4722759e02" }`   |
| `parameters` | object | It would contain the whole input payload.  | `See example below` |

##### Example of the response body

```json
{
  "job":{
    "id": "55c09c56-9f99-4da2-bba4-da4722759e08",
    "type": "MEETING_ANALYSIS",
    "relations": {
       "meeting_id": "55c09c56-9f99-4da2-bba4-da4722759e01",
       "workspace_id": "55c09c56-9f99-4da2-bba4-da4722759e02"
    },
    "parameters": {
      "channels": 1,
      "audio_start_offset": 10.5,
      "audio_format": "wav",
      "audio_sample_rate": 8000,
      "audio_encoding": "pcm_s16le",
     "diarization_options": "by_server",
     "num_speakers": 2,
     "enable_itn": true,
     "enable_punctuation": true,
      "scenario": "customer_service_call",
      "scenario_parameters": {
        "went_to_voicemail": false,
        "contains_recordings": false,
        "spoke_to_agent": true,
        "customer_number": "0933123456",
        "customer_name": "John Doe",
        "agent_name": "Jane Doe",
        "num_speakers": 2
      },
    },
    "status": "QUEUED",
    "error_message": null,
    "result": null
  }
}
```

#### Response Status 400

AudioNotFoundError

##### Status code: 400

## Get Job by ID

Query job information

### API

GET /api/v1/workspaces/{workspace_id}/jobs/{job_id}

#### Header

| Name | Value | Description |
| :---- | :---- | :---- |
| accept | application/json |  |
| Authorization | Bearer {access_token} | Bearer token |

#### Response Status 200

Normal response with the requested job data

##### Status code: 200

##### Response body

| Name | Type | Description | Example |
| :---- | :---- | :---- | :---- |
| id | string | The job id. | `55c09c56-9f99-4da2-bba4-da4722759e08` |
| type | string | The type of job. | `MEETING_ANALYSIS` |
| status | string | Indicates the status of the job `QUEUED`, `FINISHED`, `FAILED`, or `STARTED`. The analysis will be sent to callback_url after the status changes to `FINISHED` for a period of time. | `QUEUED` |
| result | null | Stay null value through all status | `See example below` |
| error_message | string | null | When an error occurs, it returns error information; otherwise, it is null if no errors occur | `null` |
| `relations` | object | It would contain two keys: “workspace_id”, “meeting_id”. All of the keys have their id. | `{"meeting_id": "55c09c56-9f99-4da2-bba4-da4722759e01", "workspace_id": "55c09c56-9f99-4da2-bba4-da4722759e02" }`   |
| `parameters` | object | It would contain the whole input payload. | See example below |

##### Example of the response body

```json
{
  "id": "55c09c56-9f99-4da2-bba4-da4722759e08",
  "type": "MEETING_ANALYSIS",
  "status": "FINISHED",
  "result": null,
  "relations": {
     "meeting_id": "55c09c56-9f99-4da2-bba4-da4722759e01",
     "workspace_id": "55c09c56-9f99-4da2-bba4-da4722759e02"
  },
  "parameters": {
    "channels": 1,
    "audio_start_offset": 10.5,
    "audio_format": "wav",
    "audio_sample_rate": 8000,
    "audio_encoding": "pcm_s16le",
    "scenario": "customer_service_call",
    "scenario_parameters": {
      "went_to_voicemail": false,
      "contains_recordings": false,
      "spoke_to_agent": true,
      "customer_number": "0933123456",
      "customer_name": "John Doe",
      "agent_name": "Jane Doe",
      "num_speakers": 2
    }
  },
  "status": "QUEUED",
  "error_message": null,
  "result": null
}
```

#### Response Status 404

The requested data does not exist.

##### Status code: 404

# Callback API

## Callback for Call Analysis

The callback API specifications for call analysis. 
***IMPORTANT***
- Each workspace has its dedicated callback url and callback metadata (optional). Please contact [info@seasalt.ai](mailto:info@seasalt.ai).
- Developers should implement their callback APIs according to the following schema to successfully accept SeaMeet analysis callbacks.  
- The key of `X-Seasalt-Server-Signature` would be provided to you we've set up your workspace with the provided callback settings.

#### Header

| name | value | Description |
| :---- | :---- | :---- |
| accept | application/json |  |
| X-Seasalt-Server-Signature | HMAC(k, m, h) m: json body in utf-8. k: each workspace having random ASCII letters (both uppercase and lowercase) and digits in total length 32\. h: sha256  The result will be presented as hexadecimal digits. | For security issue |

#### Method: POST

#### Request Body

| name | type | Description | example |
| :---- | :---- | :---- | :---- |
| payload | Payload object | Analysis results formatted in json string. | `See example below` |
| event_name | str | Should be `dashboard_analysis_finished` | `"dashboard_analysis_finished"` |
| meeting_id | string | The meeting id of analyzed meeting | `"seax_bd4aeffdf09520dd077c7e541b9ae577"` |
| workspace_id | string | The workspace id of the meeting | `"xxx"` |

#### Payload

This is an example payload with some sample analysis items like `customer_satisfaction`

| name | type | Description | example |
| :---- | :---- | :---- | :---- |
| meeting_id | string | The meeting id of analyzed meeting | `"seax_bd4aeffdf09520dd077c7e541b9ae577"` |
| customer_satisfaction_rating | string | The customer satisfaction rating during the meeting. The score ranges from `A` to `E`, with `A` representing the best and `E` the worst. If the value is `null`, it means there is insufficient information to make a judgment. | `A` |
| agent_performance_rating | string | The agent performance rating during the meeting. The score ranges from `A` to `E`, with `A` representing the best and `E` the worst. If the value is `null`, it means there is insufficient information to make a judgment.  | `A` |
| agent_performance_feedback | string | The feedback for the agent performance during the meeting  | `The agent took the initiative to inquire about and confirm the customer's needs, and provided clear instructions.` |
| risk_factor | string | The risk_factor of the meeting | `Communication difficulties` |
| summary | string | The summary of the meeting | `The customer needs to upload supplementary documents.` |
| title | string | The title(topic) of the meeting | `Issues with Customer Document Submission and Communication` |
| transcript | List of Transcript object |  |  |

#### Transcript object

| name | type | Description | example |
| :---- | :---- | :---- | :---- |
| text | string | The transcript text | `Hi, I'm calling to ....` |
| speaker | string  | The speaker name of this transcript | `test agent` |

##### 

##### Example of the request body

```json
{
  "event_name": "dashboard_analysis_finished",
  "workspace_id": "xxx",
  "meeting_id": "xxx",
  "payload": {    
        "meeting_id": "ee48e21f-2576-49bc-9272-76960ae87a72",
        "customer_satisfaction_rating": "A",
        "agent_performance_rating": "A",
        "agent_performance_feedback": "The agent took the initiative to inquire about and confirm the customer's needs, and provided clear instructions.",
        "risk_factor": "Communication difficulties",
        "summary": "The customer needs to upload supplementary documents.",
        "title": "Issues with Customer Document Submission and Communication",
        "transcript": [
            {
                "text": "Hi, I'm calling to ....",
                "speaker": "test agent"
            }
         ]

  }
}
```

# Example Python Script

Run below python script with command  `python3 import_meeting_audio.py --access-token $TOKEN --wav-path test.wav --wav-name test.wav --workspace-id $WORKSPACE_ID --seameet-url-base https://meet.seasalt.ai/seameet-api`.

```py
"""
It provides a command line interface to:
- create a meeting
- generate an upload URL for audio
- upload the audio
- start the transcription process.

Prerequisites:
- Python 3.8+
- pip install requests

Example usage:
    python import_meeting_audio.py --access-token eyxxx --workspace-id test --wav-path test.wav --wav-name test.wav
"""

import argparse
import logging
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Optional

import requests

root = logging.getLogger()
root.setLevel("DEBUG")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel("DEBUG")
formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


def main(args: argparse.Namespace):
    logging.debug("process start")
    meeting_id = _create_meeting(args)
    url = _get_meeting_upload_url(args, meeting_id)
    _upload_audio(args, url)
    _analyze_meeting_audio(args, meeting_id)

    logging.debug("process finished")


def _create_meeting(args: argparse.Namespace) -> str:
    body = {
        "meeting_name": args.meeting_name,
        "channel_type": "PHONE",
        "language": args.meeting_language,
        "start_time": args.meeting_start_time,
    }
    url = f"{args.seameet_url_base}/api/v1/workspaces/{args.workspace_id}/meetings"
    response = _query_backend_service(
        access_token=args.access_token,
        url=url,
        method="POST",
        body=body,
    )
    return response["id"]


def _get_meeting_upload_url(args: argparse.Namespace, meeting_id: str) -> str:
    body = {}
    url_parameters = {"file_name": args.wav_name}
    url = f"{args.seameet_url_base}/api/v1/workspaces/{args.workspace_id}/meetings/{meeting_id}/upload_audio_url"
    response = _query_backend_service(
        access_token=args.access_token,
        url=url,
        method="POST",
        body=body,
        url_parameters=url_parameters,
    )
    return response["upload_audio_url"]


def _upload_audio(args: argparse.Namespace, url: str):

    with open(args.wav_path, "rb") as f:
        response = requests.put(url, data=f)
        response.raise_for_status()

    logging.debug((f"uploaded {args.wav_path} to s3"))


def _analyze_meeting_audio(args: argparse.Namespace, meeting_id: str) -> str:
    body = {
        "meeting_id": meeting_id,
        "channel": 1,
        "audio_start_offset": args.audio_start_offset,
        "audio_format": args.audio_format,
        "audio_sample_rate": args.audio_sample_rate,
        "audio_encoding": args.audio_encoding,
        "scenario": args.scenario,
        "scenario_parameters": {
            "went_to_voicemail": False,
            "contains_recordings": False,
            "spoke_to_agent": False,
            "customer_number": args.customer_number,
            "customer_name": args.customer_name,
            "agent_name": args.agent_name,
            "enable_agent_recognition": args.enable_agent_recognition,
            "direction": args.direction,
        },
        "file_name": args.wav_name,
        "speaker_accounts": [],
        "diarization_options":"by_server",
        "num_speakers": 2,
        "enable_itn": True,
        "enable_punctuation": True,
        "use_existing_audio": args.use_existing_audio,
        "reset_meeting": args.reset_meeting,
        "queue_type": args.queue_type,
    }
    url = f"{args.seameet_url_base}/api/v1/workspaces/{args.workspace_id}/meetings/{meeting_id}/analyze_audio"
    _query_backend_service(
        access_token=args.access_token,
        url=url,
        method="POST",
        body=body,
    )


def _query_backend_service(
    access_token: str,
    url: str,
    method: str,
    body: dict = {},
    headers: dict = {},
    url_parameters: dict = {},
    timeout: Optional[float] = None,
) -> dict:
    start_time = time.time()
    response = None
    try:
        if url_parameters:
            url += "?" + urllib.parse.urlencode(url_parameters)
        final_headers = {
            "accept": r"application/json",
            "Content-Type": r"application/json",
            "Authorization": f"Bearer {access_token}",
        }

        if headers:
            final_headers.update(headers)
        # NOTE: Extend default timeout to wait the Backend API-Server responding.
        # - Especially the post_final_transcription is taking too long.
        session = requests.Session()
        request = requests.Request(method, url, json=body, headers=final_headers)
        response = session.send(request.prepare(), timeout=timeout)
        response.raise_for_status()
        if not response.text:
            return {}
        result_json = response.json()
        logging.debug(
            (
                f"finish a request to API server, time elapsed: {time.time()-start_time:.3f}s, method: {method}, url:{url}"
                f", method: {method}, body: {body}, response body: {result_json}"
            )
        )
        return result_json
    except Exception as e:
        logging.warning(
            (
                f"failed to request API server, time elapsed: {time.time()-start_time:.3f}s, method: {method}, url:{url}, "
                f"error: {e.__class__.__name__} {e} {response.text if response else ''}"
            )
        )
        raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workspace-id",
        dest="workspace_id",
        type=str,
        required=True,
        help="Set the workspace id.",
    )
    parser.add_argument(
        "--wav-path",
        dest="wav_path",
        type=str,
        required=True,
        help="Set the wav path.",
    )
    parser.add_argument(
        "--wav-name",
        dest="wav_name",
        type=str,
        required=True,
        help="Set the wav name.",
    )
    parser.add_argument(
        "--access-token",
        dest="access_token",
        type=str,
        required=True,
        help="The user's access token for the seameet api.",
    )
    parser.add_argument(
        "--meeting-name",
        dest="meeting_name",
        type=str,
        required=False,
        default="test meeting",
        help="Set the meeting name.",
    )
    parser.add_argument(
        "--meeting-language",
        dest="meeting_language",
        type=str,
        required=False,
        default="zh-TW",
        help="Set the meeting language.",
    )
    parser.add_argument(
        "--meeting-start-time",
        dest="meeting_start_time",
        type=str,
        required=False,
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        help="Set the meeting start time in the format of 'yyyy-mm-dd hh:mm:ss', UTC+0.",
    )
    parser.add_argument(
        "--seameet-url-base",
        dest="seameet_url_base",
        type=str,
        required=False,
        default="https://meet.seasalt.ai/seameet-api",
        help="the seameet url",
    )
    parser.add_argument(
        "--audio-start-offset",
        dest="audio_start_offset",
        type=int,
        required=False,
        default=0,
        help="indicate the audio start offset in seconds, relative to the start of the meeting.",
    )
    parser.add_argument(
        "--audio-format",
        dest="audio_format",
        type=str,
        required=False,
        default="wav",
        help="Set the audio format.",
    )
    parser.add_argument(
        "--audio-sample-rate",
        dest="audio_sample_rate",
        type=int,
        required=False,
        default=8000,
        help="Set the audio sample rate.",
    )
    parser.add_argument(
        "--audio-encoding",
        dest="audio_encoding",
        type=str,
        required=False,
        default="pcm_s8le",
        help="Set the audio encoding.",
    )
    parser.add_argument(
        "--scenario",
        dest="scenario",
        type=str,
        required=False,
        default="customer_service_call",
        help="Set the meeting scenario.",
    )
    parser.add_argument(
        "--customer-number",
        dest="customer_number",
        type=str,
        required=False,
        default="+886123456789",
        help="Set the customer number for the scenario: customer_service_call.",
    )
    parser.add_argument(
        "--customer-name",
        dest="customer_name",
        type=str,
        required=False,
        default="test customer",
        help="Set the customer name for the scenario: customer_service_call.",
    )
    parser.add_argument(
        "--agent-name",
        dest="agent_name",
        type=str,
        required=False,
        default="test agent",
        help="Set the agent name for the scenario: customer_service_call.",
    )
    parser.add_argument(
        "--direction",
        dest="direction",
        type=str,
        required=False,
        help="Set the meeting direction, INBOUND or OUTBOUND.",
    )
    parser.add_argument(
        "--enable-agent-recognition",
        dest="enable_agent_recognition",
        type=bool,
        required=False,
        default=True,
        help="enable_agent_recognition",
    )
    parser.add_argument(
        "--use-existing-audio",
        dest="use_existing_audio",
        type=bool,
        required=False,
        default=False,
        help="Use the meeting audio(all.wav) that already saved in seameet api.",
    )
    parser.add_argument(
        "--reset_meeting",
        dest="reset_meeting",
        type=bool,
        required=False,
        default=False,
        help="If it's true, it will delete all transcriptions and nlp things in the meeting before analyzing.",
    )
    parser.add_argument(
        "--queue_type",
        dest="queue_type",
        type=str,
        required=False,
        default="DEDICATED",
        help="The queue type=DEDICATED.",
    )

    args = parser.parse_args()
    main(args)
```

2. If callback server implemented and set up complete by Seasalt.ai, get the analysis callback after a few minutes.

```
== header ==
host 865b-1-172-6-216.ngrok-free.app
user-agent Python/3.8 aiohttp/3.8.1
content-length 397
accept */*
accept-encoding gzip, deflate
content-type application/json
x-forwarded-for 54.70.236.205
x-forwarded-host 865b-1-172-6-216.ngrok-free.app
x-forwarded-proto https
x-seasalt-server-signature 3ec52b15632cbb634a900c7be551c60ea799b49f0a193a8e39cd1a844585cd3a
== body ==
{'event': 'dashboard_analysis_finished'
, payload: {'meeting_id': '2394a2dd-bc25-44f9-a159-643815e55d64', 'customer_satisfaction_rating': 'A', 'agent_performance_rating': 'A', 'agent_performance_feedback': 'The agent was professional and patient during the conversation with the customer, ensuring their needs were properly addressed.', "transcript":[...]
}}

```
