---
title: Re-invite Bot
linkTitle: Re-invite Bot
description:
  Learn how to ask the SeaMeet bot to (re)join a Google Meet using the
  SeaMeet API.
type: docs
weight: 10
---

## Overview

Use this endpoint to ask the SeaMeet bot to join a meeting after the initial
auto-join did not run, or after a meeting has already ended and you want a
fresh recording session against the same Google Meet URL.

Typical use cases:

- A scheduled meeting started but no bot joined (e.g., the calendar event was
  created late or the original auto-dispatch was skipped). Call the endpoint
  to dispatch the bot right now.
- A meeting has already finished (`OFFLINE`) and you want to reuse the same
  meeting record for a follow-up recording on the same Meet URL. Call with
  `force_restart=true` to reset it back to `INITIAL` and dispatch the bot.

The endpoint enforces at most **one bot per (Meet URL, workspace)**. Calling it
multiple times while a dispatch is already in flight will return a conflict
rather than spawning a second bot.

This endpoint only supports **Google Meet** meetings. MS Teams and Zoom
meetings will be rejected with `400 meeting_channel_not_supported`.

## Authorization: API Key

All requests must include a valid API key issued from your workspace in the
`Authorization` header as a Bearer token. The calling user must have the
**Owner** or **Manager** role on the target workspace; lower roles are
rejected.

### 1. Generate Your API Key

Currently the only UI to get an API key is through
[SeaX](https://seax.seasalt.ai).

- Go to **Workspace → API Key** tab.
- Click **Add New Key** and check `seameet` as the scope.
- Copy the key and keep it safe. This key is required in the `Authorization`
  header for **all requests**.

## API Specification

### Re-invite Bot

`POST /api/v1/public/meeting/{workspace_id}/meetings/{meeting_id}/reinvite_bot`

Dispatch the SeaMeet bot for a meeting in your workspace.

| Field            | Type              | Description                                                                                                                                       | Allowed Values / Example               | Required |
| ---------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | -------- |
| `Authorization`  | `string (header)` | Bearer API key with the `seameet` scope                                                                                                           | `Bearer <your_api_key>`                | ✅       |
| `workspace_id`   | `string (path)`   | Workspace ID that owns the meeting                                                                                                                | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | ✅       |
| `meeting_id`     | `string (path)`   | Meeting ID to re-invite the bot for                                                                                                               | `2b342a6e177d4b139638bc16bd312291`     | ✅       |
| `force_restart`  | `bool (body)`     | When `true`, an `OFFLINE` meeting is reset back to `INITIAL` and a fresh bot is dispatched. When `false` (default), only `INITIAL` is dispatched. | `false`                                |          |

### Behavior by meeting status

| Current status     | `force_restart=false`                       | `force_restart=true`                            |
| ------------------ | ------------------------------------------- | ----------------------------------------------- |
| `INITIAL`          | `202` – bot dispatched                      | `202` – bot dispatched (no reset)               |
| `LIVE`             | `409 meeting_live_bot_present`              | `409 meeting_live_use_stop_first`               |
| `STOPPING`         | `409 meeting_in_cleanup`                    | `409 meeting_in_cleanup`                        |
| `ANALYZING`        | `409 meeting_in_cleanup`                    | `409 meeting_in_cleanup`                        |
| `OFFLINE`          | `409 meeting_offline_use_force_restart`     | `202` – meeting reset to `INITIAL` and bot dispatched |

The `force_restart=true` reset preserves the meeting’s configuration (language,
participants, transcriptions, NLP results, etc.) and only flips the runtime
state fields (`status`, `start_time`, `end_time`, `duration`, `flag`) so the
existing meeting can host a new bot session.

#### Example

Re-invite the bot to a meeting that is still `INITIAL`:

```bash
curl -X 'POST' \
  'https://meet.seasalt.ai/seameet-api/api/v1/public/meeting/<workspace_id>/meetings/<meeting_id>/reinvite_bot' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <your_api_key>' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Restart a meeting that has already ended (`OFFLINE`) and dispatch a fresh bot:

```bash
curl -X 'POST' \
  'https://meet.seasalt.ai/seameet-api/api/v1/public/meeting/<workspace_id>/meetings/<meeting_id>/reinvite_bot' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <your_api_key>' \
  -H 'Content-Type: application/json' \
  -d '{"force_restart": true}'
```

#### Response Status 202

The bot dispatch has been accepted. The bot will join the Google Meet shortly;
this endpoint returns as soon as the dispatch is enqueued, not when the bot
has actually joined.

```json
{
  "meeting_id": "2b342a6e177d4b139638bc16bd312291",
  "status": "INITIAL",
  "action": "dispatched",
  "dispatched_at": "2026-05-21T03:42:11.482"
}
```

| Field            | Type     | Description                                                                                              |
| ---------------- | -------- | -------------------------------------------------------------------------------------------------------- |
| `meeting_id`     | `string` | The meeting ID                                                                                           |
| `status`         | `string` | Meeting status at the moment of dispatch (always `INITIAL` on success)                                   |
| `action`         | `string` | `dispatched` if the meeting was already `INITIAL`; `restarted` if it was reset from `OFFLINE` first      |
| `dispatched_at`  | `string` | UTC timestamp when the dispatch was accepted (ISO 8601, no timezone suffix)                              |

#### Error Responses

| HTTP | `code` | Meaning                                                                                                                          |
| ---- | ------ | -------------------------------------------------------------------------------------------------------------------------------- |
| 400  | 12101  | The given `meeting_id` does not belong to the given `workspace_id`.                                                              |
| 400  | 12102  | The meeting is not a Google Meet meeting (MS Teams / Zoom are not supported by this endpoint).                                   |
| 404  | 12100  | No meeting with the given `meeting_id` exists.                                                                                   |
| 409  | 12103  | The meeting is `LIVE`; a bot is already in the room. No action needed.                                                           |
| 409  | 12104  | Refused to force-restart a `LIVE` meeting. Stop the meeting first, then retry once it is `OFFLINE`.                              |
| 409  | 12105  | The meeting is `STOPPING` or `ANALYZING`. Wait for it to reach `OFFLINE`, then retry (with `force_restart=true` if needed).      |
| 409  | 12106  | The meeting is `OFFLINE`. Pass `force_restart=true` to restart it.                                                               |
| 409  | 12107  | A dispatch for this meeting is already in flight in this workspace. Retry after the in-flight dispatch completes (≤10 minutes). |
| 409  | 12110  | The meeting status changed between the endpoint’s check and the restart. Fetch the latest meeting state and retry.               |
| 409  | 12111  | The meeting is in an unexpected status and cannot be dispatched. Inspect the meeting and contact support if this persists.       |
| 500  | 12109  | The dispatch failed for an unexpected reason. Safe to retry; contact support if it persists.                                     |
| 503  | 12108  | Another dispatch is currently holding the per-workspace lock. Retry in a few seconds.                                            |

All error responses follow the standard envelope:

```json
{
  "detail": "Meeting <meeting_id> is OFFLINE. Pass force_restart=true to restart",
  "code": 12106,
  "parameters": { "meeting_id": "2b342a6e177d4b139638bc16bd312291" }
}
```
