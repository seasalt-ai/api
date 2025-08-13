---
title: SeaMeet API Documentation
linkTitle: SeaMeet API
type: docs
menu: {main: {weight: 30}}
---

## Overview
SeaMeet API provides powerful tools for managing meetings, processing audio recordings, and generating intelligent meeting insights. This API enables developers to integrate advanced meeting management features including real-time transcription, speaker diarization, and automated meeting summarization.

## Key Features

### Meeting Management
- Create and manage meetings from audio recordings
- Support for Google Meet integration and uploaded audio files
- Automatic detection of meeting participants and speakers

### Audio Processing
- High-accuracy speech-to-text transcription
- Multi-language support with dialect recognition
- Speaker separation and identification (diarization)

### Intelligent Insights
- Automated meeting summaries with action items
- Conversation analytics and participation metrics
- Customizable summary templates

### Integration Support
- Webhook notifications for meeting status updates
- Real-time transcription streaming
- Export capabilities for transcripts and summaries

## Getting Started

### Prerequisites
1. Create a SeaMeet workspace through the [SeaMeet Dashboard](https://meet.seasalt.ai). If you don't have an account yet, sign up [here](https://meet.seasalt.ai/signup)
2. Follow steps [here]({{< relref "Portal/_index.md#Prerequisites" >}}) to generate your API key (make sure to select `SeaMeet` in the `Scope` when adding new keys)
3. Install required client libraries or use REST API directly

## Authentication

All interactions with the SeaMeet API require proper authentication using Bearer token authentication. This security mechanism ensures that only authorized applications and users can access your workspace and agent data.

### Bearer Token Authentication

Every API request must include an Authorization header with your API key formatted as a Bearer token. The header format is:

```
Authorization: Bearer [your-access-token]
```

Replace `[your-access-token]` with your actual API key. This token provides full access to your workspace, so it should be treated as a sensitive credential.
