---
title: Analytics
linkTitle: Analytics API Tutorial
type: docs
weight: 2
---

## Overview

The Analytics endpoint provides a unified interface for retrieving workspace-level analytics across various metrics, including message activity, call volume, label usage, and conversation summaries. By submitting structured query parameters, you can generate detailed reports based on custom time ranges, aggregation units (day, month, year), and filters such as labels or handling status. The endpoint supports multiple metric types, each returning structured and contextualized data to help you monitor performance, identify trends, and make data-driven decisions. Authentication via API key is required to ensure secure access to workspace data.

You can also access the RESTful API docs of Event Webhooks [here](./Docs/notify-api/)

---

#### Endpoint

`POST https://portal.seasalt.ai/portal-api/api/v1/analytics/generate_analytics`

Use this endpoint to register a webhook that will receive event notifications
from Portal.
#### Allowed Fields in Request Body

This section lists all available fields that can be included in the request body when calling the `/generate_analytics` endpoint. While these fields are supported by the API, **not all of them are required for every metric**. The combination of fields you need to provide depends on the specific `metric` you're requesting. Please refer to the metric-specific sections below to see which fields are required or optional for each case:

- [`TODAY_COMMUNICATION_VOLUME`](#metric-today_communication_volume)  
- [`ACTIVITY_TREND`](#metric-activity_trend)  
- [`LABEL_USAGE`](#metric-label_usage)  
- [`CONVERSATION_OVERVIEW`](#metric-conversation_overview)  
- [`TOTAL_USAGE`](#metric-total_usage)  
- [`SEACHAT_CONVERSATION_OVERVIEW`](#metric-seachat_conversation_overview)  
- [`SEACHAT_CONVERSATION_OVERVIEW_YEARLY`](#metric-seachat_conversation_overview_yearly)  
- [`SEACHAT_CONVERSATION_BREAKDOWN`](#metric-seachat_conversation_breakdown)

| Field                    | Type                         | Required | Description                                                 | Allowed Values / Example                                                                                                                                                                                         |
| ------------------------ | ---------------------------- | -------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metric`                 | `string`                     | ✅       | Type of analytics data to retrieve                          | `today_communication_volume`, `activity_trend`, `label_usage`, `conversation_overview`, `total_usage`, `seachat_conversation_overview`, `seachat_conversation_overview_yearly`, `seachat_conversation_breakdown` |
| `type`                   | `string`                     |          | Whether to analyze messages or calls (used in some metrics) | `messages`, `calls`                                                                                                                                                                                              |
| `time_unit`              | `string`                     |          | Aggregation level for data                                  | `day`, `month`, `year`                                                                                                                                                                                           |
| `timezone`               | `string`                     |          | Timezone used for grouping and filtering                    | Example: `UTC`, `Asia/Taipei`                                                                                                                                                                                    |
| `range_type`             | `string`                     |          | Predefined time range                                       | `last_day`, `last_7_days`, `last_30_days`, `last_90_days`, `last_180_days`                                                                                                                                       |
| `exclude_empty_response` | `boolean`                    |          | Exclude conversations with no bot or agent replies          | `true`, `false`                                                                                                                                                                                                  |
| `from_date`              | `string (ISO 8601 datetime)` |          | Custom start of the date range                              | Example: `2024-05-01T00:00:00`                                                                                                                                                                                   |
| `to_date`                | `string (ISO 8601 datetime)` |          | Custom end of the date range                                | Example: `2024-05-31T23:59:59`                                                                                                                                                                                   |
| `labels`                 | `array of strings`           |          | Filter by label names                                       | Example: `["support", "sales"]`                                                                                                                                                                                  |
| `handling_status`        | `string`                     |          | Filter conversations by handling status                     | `RESOLVED`, `PENDING`, `FOLLOW_UP`                                                                                                                                                                               |
| `year`                   | `string (YYYY)`              |          | Year for yearly report metrics                              | Example: `2024`                                                                                                                                                                                                  |


#### Authorization

You must provide your API key in the `X-API-KEY` header.

#### Metrics
##### Metric: TODAY_COMMUNICATION_VOLUME
This metric provides a **summary of today’s communication activity**. It shows how many inbound and outbound voice calls were made, along with the number of non-voice (e.g., chat) messages received. Use this to get a quick snapshot of how busy your workspace is today.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric = today_communication_volume`  | `✅` | Always required |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | `today_communication_volume` |
| `time_unit` | `string` | `day` |
| `data` | `array` of `object` | Contains a single summary object representing today's communication volume |
| `data[].inbound_voice_count` | `integer` | Number of inbound voice calls received today |
| `data[].outbound_voice_count` | `integer` | Number of outbound voice calls made today |
| `data[].inbound_non_voice_count` | `integer` | Number of inbound non-voice messages (e.g., chat, text) received today |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
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
This metric tracks **how your communication activity changes over time**. You can choose to analyze either messages or calls, grouped by day, month, or year. It helps you identify trends in user engagement, support load, and agent activity — with breakdowns by sender type or call direction, plus percent change from the previous period.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric` \= `activity_trend` | ✅ | Always required |
| `type` | ✅ | `messages`, `calls` |
| `time_unit` | ✅ | `day`,  `month`,  `year` |
| `from_date` | ✖️Defaults to the beginning of today | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |
| `to_date` | ✖️Defaults to today’s end time | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"activity_trend"` |
| `time_unit` | `string` | The time unit for grouping: `day`, `month`, or `year` |
| `data` | `array of object` | One object per time period, grouped by `period` |
| `data[].period` | `string` | The date or time period (e.g., `"2024-06-01"`) |
| `data[].CUSTOMER` | `integer` | Number of messages sent by end users |
| `data[].AGENT` | `integer` | Number of messages sent by agents |
| `data[].BOT` | `integer` | Number of messages sent by bots  |
| `data[].SYSTEM` | `integer` | Number of system messages  |
| `data[].inbound` | `integer` | Number of inbound call sessions |
| `data[].outbound` | `integer` | Number of outbound call sessions |
| `change_percent` | `float` | % change vs. the previous period total (rounded to 2 decimals) |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
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
      "period": "2024-06-01",
      "CUSTOMER": 45,
      "AGENT": 60,
      "bot": 20
    },
    {
      "period": "2024-06-02",
      "CUSTOMER": 30,
      "AGENT": 55,
      "BOT": 15,
    },
    {
      "period": "2024-06-03",
      "CUSTOMER": 50,
      "AGENT": 70,
      "BOT": 25
    }
  ],
  "change_percent": 12.5
}
```


##### Metric: LABEL_USAGE
Returns label usage statistics over time, grouped by the specified `time_unit` (e.g., day, month, year). Each time period contains a list of labels and how many times each was used.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric` \= `label_usage` | ✅ | Always required |
| `time_unit` | `✅` | `day,  month,  year` |
| `labels` | ✖️ Defaults to return all labels if not provided | Optional filtering by labels names |
| `from_date` | ✖️Defaults to the beginning of today | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |
| `to_date` | ✖️Defaults to today’s end time | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"label_usage"` |
| `time_unit` | `string` | The time grouping used in the request (`day`, `month`, or `year`) |
| `data` | `array of object` | Each object represents one time period |
| `data[].period` | `string` | The time period label (e.g., `"2024-06"`) |
| `data[].labels` | `array of object` | List of labels and their usage count during the period |
| `data[].labels[].name` | `string` | Label name (e.g., `"support"`) |
| `data[].labels[].count` | `integer` | Number of times the label was applied in that period |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
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
      "period": "2024-06",
      "labels": [
        { "name": "sales", "count": 45 },
        { "name": "support", "count": 32 }
      ]
    },
{
      "period": "2024-05",
      "labels": [
        { "name": "sales", "count": 15 },
        { "name": "support", "count": 27 }
      ]
    }

  ]
}
```

##### Metric: TOTAL_USAGE
Returns a **summary of total usage** over a specified time range, including total voice call duration and number of chat messages.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric` \= `total_usage` | ✅ | Always required |
| `from_date` | ✖️Defaults to the beginning of today | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |
| `to_date` | ✖️Defaults to today’s end time | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"total_usage"` |
| `time_unit` | `string` | The time unit used for aggregation (e.g., `day`, `month`, `year`) |
| `data` | `array of object` | Usually contains only one object per request |
| `data[].total_voice_minutes` | `number` | Total duration of voice calls (in minutes) |
| `data[].total_chat_responses` | `integer` | Total number of chat messages sent by bots or agents |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
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
Returns the **total number of conversations** per time period (e.g., by month), allowing you to track conversation volume trends.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric` \= `conversation_overview` | ✅ | Always required |
| `time_unit` | ✅ | Aggregation unit |
| `handling_status` | ✖️ Defaults to return all conversations regardless of handling status | `RESOLVED`, `PENDING`, `FOLLOW_UP` |
| `from_date` | ✖️Defaults to the beginning of today | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |
| `to_date` | ✖️Defaults to today’s end time | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"conversation_overview"` |
| `time_unit` | `string` | The time unit used for grouping (e.g., `day`, `month`, `year`) |
| `data` | `array of object` | Each object represents one time period |
| `data[].period` | `string` | The label for the time period (e.g., `"2024-06"`) |
| `data[].count` | `integer` | Number of conversations in that time period |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
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
      "period": "2024-06",
      "count": 200
    },
  {
      "period": "2024-05",
      "count": 180
    }
  ]
}
```


##### Metric: SEACHAT_CONVERSATION_OVERVIEW
Provides a comprehensive **summary of SeaChat activity** within a selected time range, including message counts, live agent requests, and period-over-period comparisons.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric` \= `seachat_conversation_overview` | ✅ | Always required |
| `timezone` | ✖️ Defaults to UTC  | User timezone, defaults to UTC |
| `range_type` | ✖️Defaults to last\_7\_days | `last_day,  Last_7_days, Last_30_days, last_90_days, last_180_days` |
| `exclude_empty_response` | ✖️ Defaults to false | Optional, True or False |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"seachat_conversation_overview"` |
| `conversations` | `integer` | Total number of conversations during the current period |
| `messages` | `integer` | Total number of messages (all sources) |
| `bot_messages` | `integer` | Messages sent by bots |
| `agent_messages` | `integer` | Messages sent by human agents |
| `live_agent_requests` | `integer` | Number of live agent hand-off requests |
| `distinct_user_count` | `integer` | Unique users who participated in conversations |
| `conversations_change_percentage` | `float` | % change in conversation count compared to previous period |
| `messages_change_percentage` | `float` | % change in message volume |
| `bot_messages_change_percentage` | `float` | % change in bot messages |
| `agent_messages_change_percentage` | `float` | % change in agent messages |
| `live_agent_requests_change_percentage` | `float` | % change in agent requests |
| `current_period_start` | `string (datetime)` | Start time of the current analysis period |
| `current_period_end` | `string (datetime)` | End time of the current analysis period |
| `previous_period_start` | `string (datetime)` | Start time of the comparison period |
| `previous_period_end` | `string (datetime)` | End time of the comparison period |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "seachat_conversation_overview",
    "timezone": "UTC",
    "range_type": "last_7_days",
    "exclude_empty_response": true
  }'
```

**Sample Successful Response**
```javascript
{
  "metric": "SEACHAT_CONVERSATION_OVERVIEW",
  "conversations": 180,
  "messages": 900,
  "bot_messages": 400,
  "agent_messages": 300,
  "live_agent_requests": 60,
  "distinct_user_count": 120,
  "conversations_change_percentage": 10.5,
  "messages_change_percentage": 5.0,
  "bot_messages_change_percentage": 8.0,
  "agent_messages_change_percentage": 12.0,
  "live_agent_requests_change_percentage": 15.0,
  "current_period_start": "2024-06-01T00:00:00",
  "current_period_end": "2024-06-30T23:59:59",
  "previous_period_start": "2024-05-01T00:00:00",
  "previous_period_end": "2024-05-31T23:59:59"
}
```


##### Metric: SEACHAT_CONVERSATION_OVERVIEW_YEARLY
Provides a **yearly summary** of SeaChat usage, including total conversations, message volume, and a month-by-month breakdown.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric = seachat_conversation_overview_yearly`  | ✅ | Always required |
| `year` | ✖️ Defaults to this year | string (YYYY) |
| `timezone` | ✖️Defaults to UTC  | User timezone, defaults to UTC |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"seachat_conversation_overview_yearly"` |
| `total_conversations` | `integer` | Total number of conversations during the year |
| `total_messages` | `integer` | Total number of messages during the year |
| `average_messages_per_conversation` | `float` | Average number of messages per conversation |
| `monthly_messages` | `object` | A map of month names to message counts |
| `monthly_messages.<month>` | `integer` | Number of messages sent in that month (e.g., `"January": 600`) |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "seachat_conversation_overview_yearly",
    "timezone": "UTC",
    "year": "2025"
  }'
```

**Sample Successful Response**
```javascript
{
  "metric": "seachat_conversation_overview_yearly",
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


##### Metric: SEACHAT_CONVERSATION_BREAKDOWN
This metric provides a detailed breakdown of SeaChat activity over a specified time range. It includes the number of messages sent on each day of the week and hour of the day, as well as inbound message counts and unique user counts across different channels (e.g., WebChat, Messenger). This is useful for identifying peak traffic periods and understanding channel usage patterns.

**Request Body**
| Field | Required | Notes |
| :---- | :---- | :---- |
| `metric` \= `seachat_conversation_breakdown` | ✅ | Always required |
| `timezone` | ✖️ Defaults to UTC  | User timezone, defaults to UTC |
| `from_date` | ✖️Defaults to the beginning of today | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |
| `to_date` | ✖️Defaults to today’s end time | `string` (ISO 8601 datetime), e.g. 2024-06-01T00:00:00Z |

**Response**
| Field | Type | Description |
| :---- | :---- | :---- |
| `metric` | `string` | Always `"seachat_conversation_breakdown"` |
| `channel_summary` | `object` | Mapping of channel types (e.g., `WebChat`, `Messenger`) to usage stats |
| `channel_summary.<channel>.user_count` | `integer` | Number of unique inbound users per channel |
| `channel_summary.<channel>.inbound_message_count` | `integer` | Total inbound messages per channel |
| `messages_by_day` | `object` | Number of messages per day of the week |
| `messages_by_day.<day>` | `integer` | Message count for each weekday (`Monday` through `Sunday`) |
| `messages_by_hour` | `object` | Number of messages per hour (24-hour format) |
| `messages_by_hour.<hour>` | `integer` | Message count for each hour of the day (`0` through `23`) |

**Sample Request**
```javascript
curl -X POST https://portal.seasalt.ai/notify/api/v1/generate_analytics \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "seachat_conversation_breakdown",
    "timezone": "UTC",
"from_date": "2024-06-01T00:00:00",
    "to_date": "2024-06-03T23:59:59"

  }'
```

**Sample Successful Response**
```javascript
{
  "metric": "seachat_conversation_breakdown",
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

