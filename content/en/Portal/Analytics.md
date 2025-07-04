---
title: Analytics
linkTitle: Analytics API Tutorial
description: Overview and documentation entry point for the Analytics API.
type: docs
weight: 2
---

## Overview

The Analytics endpoint provides a unified interface for retrieving
workspace-level analytics across various metrics, including message activity,
call volume, label usage, and conversation summaries. By submitting structured
query parameters, you can generate detailed reports based on custom time ranges,
aggregation units (day, month, year), and filters such as labels or handling
status. The endpoint supports multiple metric types, each returning structured
and contextualized data to help you monitor performance, identify trends, and
make data-driven decisions. Authentication via API key is required to ensure
secure access to workspace data.

You can also access the RESTful API docs [here](./Docs/portal-api/)

---

#### Endpoint

`POST https://portal.seasalt.ai/portal-api/api/v1/analytics/generate_analytics`

Use this endpoint to register a webhook that will receive event notifications
from Portal.

#### Allowed Fields in Request Body

This section lists all available fields that can be included in the request body
when calling the `/generate_analytics` endpoint. While these fields are
supported by the API, **not all of them are required for every metric**. The
combination of fields you need to provide depends on the specific `metric`
you're requesting. Please refer to the metric-specific sections below to see
which fields are required or optional for each case:

- [`TODAY_COMMUNICATION_VOLUME`](#metric-today_communication_volume)
- [`ACTIVITY_TREND`](#metric-activity_trend)
- [`LABEL_USAGE`](#metric-label_usage)
- [`CONVERSATION_OVERVIEW`](#metric-conversation_overview)
- [`TOTAL_USAGE`](#metric-total_usage)
- [`CONVERSATION_OVERVIEW`](#metric-conversation_overview)
- [`CONVERSATION_OVERVIEW_YEARLY`](#metric-conversation_overview_yearly)
- [`CONVERSATION_BREAKDOWN`](#metric-conversation_breakdown)

| Field                    | Type                         | Required | Description                                                 | Allowed Values / Example                                                                                                                                                                 |
| ------------------------ | ---------------------------- | -------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metric`                 | `string`                     | ✅       | Type of analytics data to retrieve                          | `today_communication_volume`, `activity_trend`, `label_usage`, `conversation_overview`, `total_usage`, `conversation_overview`, `conversation_overview_yearly`, `conversation_breakdown` |
| `type`                   | `string`                     |          | Whether to analyze messages or calls (used in some metrics) | `messages`, `calls`                                                                                                                                                                      |
| `time_unit`              | `string`                     |          | Aggregation level for data                                  | `day`, `month`, `year`                                                                                                                                                                   |
| `timezone`               | `string`                     |          | Timezone used for grouping and filtering                    | Example: `UTC`, `Asia/Taipei`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)                                                 |
| `range_type`             | `string`                     |          | Predefined time range                                       | `last_day`, `last_7_days`, `last_30_days`, `last_90_days`, `last_180_days`                                                                                                               |
| `exclude_empty_response` | `boolean`                    |          | Exclude conversations with no bot or agent replies          | `true`, `false`                                                                                                                                                                          |
| `from_date`              | `string (ISO 8601 datetime)` |          | Custom start of the date range                              | Example: `2024-05-01T00:00:00`                                                                                                                                                           |
| `to_date`                | `string (ISO 8601 datetime)` |          | Custom end of the date range                                | Example: `2024-05-31T23:59:59`                                                                                                                                                           |
| `labels`                 | `array of strings`           |          | Filter by label names                                       | Example: `["support", "sales"]`                                                                                                                                                          |
| `handling_status`        | `string`                     |          | Filter conversations by handling status                     | `RESOLVED`, `PENDING`, `FOLLOW_UP`                                                                                                                                                       |
| `year`                   | `string (YYYY)`              |          | Year for yearly report metrics                              | Example: `2024`                                                                                                                                                                          |

#### Authorization

You must provide your API key in the `X-API-KEY` header.

To set up your API Key

- Go to **Settings → API Key** tab.

- Click **Add New Key** and check `SeaContact` as the scope.

- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

#### Metrics

##### Metric: TODAY_COMMUNICATION_VOLUME

This metric provides a **summary of today’s communication activity**. It shows
how many inbound and outbound voice calls were made, along with the number of
non-voice (e.g., chat) messages received. Use this to get a quick snapshot of
how busy your workspace is today.


**What does “today” mean?**

In this metric, **"Today" refers to the current day in the specified timezone**. If you pass a timezone in your API request (e.g., `"America/Los_Angeles"`), "Today" means midnight to now in that timezone. If you do **not** provide a timezone, the default is **UTC**, meaning "Today" spans from midnight UTC to the current UTC time.

Using a timezone ensures the metric reflects your **local business day**, making the data more aligned with your reporting or operational needs.

**How often is this metric updated?**

This metric is updated **in real time** as new messages and calls are received.

* For live dashboards, we recommend calling this API **every 10 to 15 minutes**.

* For daily summaries or reports, calling it **once near the end of the day** (e.g., just before midnight in your local timezone provided or UTC) gives the most complete view of the day’s activity.

**Request Body**

| Field    | Required | Notes                                                   |
| -------- | -------- | ------------------------------------------------------- |
| `metric` | ✅       | Always required. Must be `"today_communication_volume"` |
| `timezone`  | ✖️       | Defaults to UTC. User timezone, e.g. `"Asia/Taipei"`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

**Response**

| Field                            | Type              | Description                                                                                    |
| -------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| `metric`                         | `string`          | Always `"today_communication_volume"`                                                          |
| `time_unit`                      | `string`          | Always `"day"`                                                                                 |
| `data`                           | `array of object` | Contains a single summary object representing today's communication volume                     |
| `data[].inbound_voice_count`     | `integer`         | Number of inbound voice calls received today                                                   |
| `data[].outbound_voice_count`    | `integer`         | Number of outbound voice calls made today                                                      |
| `data[].inbound_non_voice_count` | `integer`         | Number of inbound non-voice messages (e.g. messages with text, images, and etc) received today |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "today_communication_volume"
  }'
```

**Sample Successful Response**

```javascript
{
  "metric": "today_communication_volume",
  "time_unit": "day",
  "data": [
    {
      "inbound_voice_count": 12,
      "outbound_voice_count": 5,
      "inbound_non_voice_count": 180
    }
  ]
}
```

##### Metric: ACTIVITY_TREND

This metric tracks **how your communication activity changes over time**. You
can choose to analyze either messages or calls, grouped by day, month, or year.
It helps you identify trends in user engagement, support load, and agent
activity — with breakdowns by sender type or call direction, plus percent change
from the previous period.

**Request Body**

| Field       | Required | Notes                                                                                         |
| ----------- | -------- | --------------------------------------------------------------------------------------------- |
| `metric`    | ✅       | Always required. Must be `"activity_trend"`.                                                  |
| `type`      | ✅       | `messages`, `calls`                                                                           |
| `time_unit` | ✅       | `day`, `month`, `year`                                                                        |
| `from_date` | ✖️       | Defaults to the beginning of today. `string` (ISO 8601 datetime), e.g. `2024-06-01T00:00:00Z` |
| `to_date`   | ✖️       | Defaults to today’s end time. `string` (ISO 8601 datetime), e.g. `2024-06-01T23:59:59Z`       |
| `timezone`  | ✖️       | Defaults to UTC. User timezone, e.g. `"Asia/Taipei"`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

**Response**

| Field             | Type              | Description                                                      |
| ----------------- | ----------------- | ---------------------------------------------------------------- |
| `metric`          | `string`          | Always `"activity_trend"`                                        |
| `time_unit`       | `string`          | The time unit for grouping: `day`, `month`, or `year`            |
| `data`            | `array of object` | One object per time period, grouped by `date`                  |
| `data[].date`   | `string`          | The date or time period (e.g., `"2024-06-01"`)                   |
| `data[].CUSTOMER` | `integer`         | Number of messages sent by end users                             |
| `data[].AGENT`    | `integer`         | Number of messages sent by human agents                          |
| `data[].BOT`      | `integer`         | Number of messages sent by bots                                  |
| `data[].SYSTEM`   | `integer`         | Number of system messages such as "switched to human agent mode" |
| `data[].inbound`  | `integer`         | Number of inbound call sessions                                  |
| `data[].outbound` | `integer`         | Number of outbound call sessions                                 |
| `change_percent`  | `float`           | % change vs. the previous period total (rounded to 2 decimals)   |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "activity_trend",
    "type": "messages",
    "time_unit": "day",
    "from_date": "2024-06-01T00:00:00",
    "to_date": "2024-06-03T23:59:59"
  }'
```

**Sample Successful Response**

```javascript
{
  "metric": "activity_trend",
  "time_unit": "day",
  "data": [
    {
      "date": "2024-06-01",
      "CUSTOMER": 45,
      "AGENT": 60,
      "bot": 20
    },
    {
      "date": "2024-06-02",
      "CUSTOMER": 30,
      "AGENT": 55,
      "BOT": 15,
    },
    {
      "date": "2024-06-03",
      "CUSTOMER": 50,
      "AGENT": 70,
      "BOT": 25
    }
  ],
  "change_percent": 12.5
}
```

##### Metric: LABEL_USAGE

Returns label usage statistics over time, grouped by the specified `time_unit`
(e.g., day, month, year). Each time period contains a list of labels and how
many times each was used.

**Request Body**

| Field       | Required | Notes                                                                                         |
| ----------- | -------- | --------------------------------------------------------------------------------------------- |
| `metric`    | ✅       | Always required. Must be `"label_usage"`                                                      |
| `time_unit` | ✅       | `day`, `month`, `year`                                                                        |
| `labels`    | ✖️       | Optional filtering by label names. Defaults to return all labels if not provided              |
| `from_date` | ✖️       | `string` (ISO 8601 datetime), e.g. `2024-06-01T00:00:00Z`. Defaults to the beginning of today |
| `to_date`   | ✖️       | `string` (ISO 8601 datetime), e.g. `2024-06-01T00:00:00Z`. Defaults to today’s end time       |
| `timezone`  | ✖️       | Defaults to UTC. User timezone, e.g. `"Asia/Taipei"`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

**Response**

| Field                   | Type              | Description                                                       |
| ----------------------- | ----------------- | ----------------------------------------------------------------- |
| `metric`                | `string`          | Always `"label_usage"`                                            |
| `time_unit`             | `string`          | The time grouping used in the request (`day`, `month`, or `year`) |
| `data`                  | `array of object` | Each object represents one time period                            |
| `data[].date`         | `string`          | The time period label (e.g., `"2024-06"`)                         |
| `data[].labels`         | `array of object` | List of labels and their usage count during the period            |
| `data[].labels[].name`  | `string`          | Label name (e.g., `"support"`)                                    |
| `data[].labels[].count` | `integer`         | Number of times the label was applied in that period              |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "label_usage",
    "time_unit": "month",
    "from_date": "2024-05-01T00:00:00",
    "to_date": "2024-06-01T23:59:59"
    "labels": ["sales", "support"]
  }'
```

**Sample Successful Response**

```javascript
{
  "metric": "label_usage",
  "time_unit": "month",
  "data": [
    {
      "date": "2024-06",
      "labels": [
        { "name": "sales", "count": 45 },
        { "name": "support", "count": 32 }
      ]
    },
{
      "date": "2024-05",
      "labels": [
        { "name": "sales", "count": 15 },
        { "name": "support", "count": 27 }
      ]
    }

  ]
}
```

##### Metric: TOTAL_USAGE

Returns a **summary of total usage** over a specified time range, including
total voice call duration and number of chat messages.

**Request Body**

| Field       | Required | Notes                                                                                         |
| ----------- | -------- | --------------------------------------------------------------------------------------------- |
| `metric`    | ✅       | Always required. Must be `"total_usage"`.                                                     |
| `from_date` | ✖️       | Defaults to the beginning of today. `string` (ISO 8601 datetime), e.g. `2024-06-01T00:00:00Z` |
| `to_date`   | ✖️       | Defaults to today’s end time. `string` (ISO 8601 datetime), e.g. `2024-06-01T23:59:59Z`       |
| `timezone`  | ✖️       | Defaults to UTC. User timezone, e.g. `"Asia/Taipei"`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

**Response**

| Field                         | Type              | Description                                                       |
| ----------------------------- | ----------------- | ----------------------------------------------------------------- |
| `metric`                      | `string`          | Always `"total_usage"`.                                           |
| `time_unit`                   | `string`          | The time unit used for aggregation (e.g., `day`, `month`, `year`) |
| `data`                        | `array of object` | Usually contains only one object per request                      |
| `data[].total_voice_minutes`  | `number`          | Total duration of voice calls (in minutes)                        |
| `data[].total_chat_responses` | `integer`         | Total number of chat messages sent by bots or agents              |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "total_usage",
    "time_unit": "month",
    "from_date": "2024-06-01T00:00:00",
    "to_date": "2024-06-03T23:59:59"
  }'
```

**Sample Successful Response**

```javascript
{
  "metric": "total_usage",
  "time_unit": "month",
  "data": [
    {
      "total_voice_minutes": 220,
      "total_chat_responses": 310
    }
  ]
}
```

##### Metric: CONVERSATION_OVERVIEW

Returns the **total number of conversations** per time period (e.g., by month),
allowing you to track conversation volume trends.

**Request Body**

| Field             | Required | Notes                                                                                                           |
| ----------------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `metric`          | ✅       | Always required. Must be `"conversation_overview"`.                                                             |
| `time_unit`       | ✅       | Aggregation unit                                                                                                |
| `handling_status` | ✖️       | Defaults to return all conversations regardless of handling status. Options: `RESOLVED`, `PENDING`, `FOLLOW_UP` |
| `from_date`       | ✖️       | Defaults to the beginning of today. `string` (ISO 8601 datetime), e.g. `2024-06-01T00:00:00Z`                   |
| `to_date`         | ✖️       | Defaults to today’s end time. `string` (ISO 8601 datetime), e.g. `2024-06-01T00:00:00Z`                         |
| `timezone`  | ✖️       | Defaults to UTC. User timezone, e.g. `"Asia/Taipei"`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

**Response**

| Field           | Type              | Description                                                    |
| --------------- | ----------------- | -------------------------------------------------------------- |
| `metric`        | `string`          | Always `"conversation_overview"`                               |
| `time_unit`     | `string`          | The time unit used for grouping (e.g., `day`, `month`, `year`) |
| `data`          | `array of object` | Each object represents one time period                         |
| `data[].date` | `string`          | The label for the time period (e.g., `"2024-06"`)              |
| `data[].count`  | `integer`         | Number of conversations in that time period                    |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "conversation_overview",
    "time_unit": "month",
    "from_date": "2024-05-01T00:00:00",
    "to_date": "2024-06-01T23:59:59",
    "handling_status::"RESOLVED"
  }'
'

```

**Sample Successful Response**

```javascript
{
  "metric": "conversation_overview",
  "time_unit": "month",
  "data": [
    {
      "date": "2024-06",
      "count": 200
    },
  {
      "date": "2024-05",
      "count": 180
    }
  ]
}
```

##### Metric: CONVERSATION_OVERVIEW_YEARLY

Provides a **yearly summary** of conversation usage, including total
conversations, message volume, and a month-by-month breakdown.

**Request Body**

| Field                                   | Required | Notes                                                                                                                      |
| --------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| `metric = conversation_overview_yearly` | ✅       | Always required. Must be `"conversation_overview_yearly"`.                                                                 |
| `year`                                  | ✖️       | Defaults to this year, format: `YYYY`                                                                                      |
| `timezone`                              | ✖️       | Defaults to UTC, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

**Response**

| Field                               | Type    | Description                                                    |
| ----------------------------------- | ------- | -------------------------------------------------------------- |
| `metric`                            | string  | Always `"conversation_overview_yearly"`                        |
| `total_conversations`               | integer | Total number of conversations during the year                  |
| `total_messages`                    | integer | Total number of messages during the year                       |
| `average_messages_per_conversation` | float   | Average number of messages per conversation                    |
| `monthly_messages`                  | object  | A map of month names to message counts                         |
| `monthly_messages.<month>`          | integer | Number of messages sent in that month (e.g., `"January": 600`) |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "conversation_overview_yearly",
    "timezone": "UTC",
    "year": "2025"
  }'
```

**Sample Successful Response**

```javascript
{
  "metric": "conversation_overview_yearly",
  "total_conversations": 1450,
  "total_messages": 8700,
  "average_messages_per_conversation": 6.0,
  "monthly_messages": {
    "January": 600,
    "February": 580,
    "March": 720
  }
}
```

##### Metric: CONVERSATION_BREAKDOWN

This metric provides a detailed breakdown of conversation activity over a
specified time range. It includes the number of messages sent on each day of the
week and hour of the day, as well as inbound message counts and unique user
counts across different channels (e.g., WebChat, Messenger). This is useful for
identifying peak traffic periods and understanding channel usage patterns.

**Request Body**

| Field       | Required | Notes                                                                                                                                                           |
| ----------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metric`    | ✅       | Always required. Must be `"conversation_breakdown"`                                                                                                             |
| `timezone`  | ✖️       | Defaults to UTC. User timezone, e.g. `"Asia/Taipei"`, see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |
| `from_date` | ✖️       | Defaults to the beginning of today. ISO 8601 (UTC), e.g. `2024-06-01T00:00:00Z`                                                                                 |
| `to_date`   | ✖️       | Defaults to today’s end time. ISO 8601 (UTC), e.g. `2024-06-01T23:59:59Z`                                                                                       |

**Response**

| Field                                             | Type      | Description                                                            |
| ------------------------------------------------- | --------- | ---------------------------------------------------------------------- |
| `metric`                                          | `string`  | Always `"conversation_breakdown"`                                      |
| `channel_summary`                                 | `object`  | Mapping of channel types (e.g., `WebChat`, `Messenger`) to usage stats |
| `channel_summary.<channel>.user_count`            | `integer` | Number of unique inbound users per channel                             |
| `channel_summary.<channel>.inbound_message_count` | `integer` | Total inbound messages per channel                                     |
| `messages_by_day`                                 | `object`  | Number of messages per day of the week                                 |
| `messages_by_day.<day>`                           | `integer` | Message count for each weekday (`Monday` through `Sunday`)             |
| `messages_by_hour`                                | `object`  | Number of messages per hour (24-hour format)                           |
| `messages_by_hour.<hour>`                         | `integer` | Message count for each hour of the day (`0` through `23`)              |

**Sample Request**

```javascript
curl -X POST https://portal.seasalt.ai/portal-api/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "conversation_breakdown",
    "timezone": "UTC",
    "from_date": "2024-06-01T00:00:00",
    "to_date": "2024-06-03T23:59:59"
  }'
```

**Sample Successful Response**

```javascript
{
  "metric": "conversation_breakdown",
  "channel_summary": {
    "WebChat": {
      "user_count": 45,
      "inbound_message_count": 320
    },
    "Messenger": {
      "user_count": 20,
      "inbound_message_count": 150
    }
  },
  "messages_by_day": {
    "Monday": 60,
    "Tuesday": 80,
    "Wednesday": 75,
    "Thursday": 90,
    "Friday": 100,
    "Saturday": 40,
    "Sunday": 25
  },
  "messages_by_hour": {
    "0": 5,
    "1": 2,
    "2": 0,
    "3": 1,
    "4": 3,
    "5": 8,
    "6": 12,
    "7": 20,
    "8": 30,
    "9": 40,
    "10": 50,
    "11": 60,
    "12": 45,
    "13": 35,
    "14": 28,
    "15": 22,
    "16": 18,
    "17": 15,
    "18": 10,
    "19": 8,
    "20": 5,
    "21": 4,
    "22": 2,
    "23": 1
  }
}
```
