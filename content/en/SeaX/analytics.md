---
title: Seasalt.ai Analytics API
linkTitle: Workspace Analytics Report
description:
  Comprehensive API documentation for the SeaX Analytics Generate Metric Report
  endpoint, enabling bulk retrieval of multiple analytics metrics in a single
  request for efficient workspace performance monitoring and reporting.
type: docs
weight: 5
---

## Overview

The Generate Metric Report endpoint provides a unified interface for retrieving
multiple analytics metrics in a single request, streamlining the process of
generating comprehensive reports for workspace performance analysis. Unlike
individual metric endpoints, this bulk endpoint allows you to request multiple
analytics types simultaneously, reducing API calls and improving efficiency for
dashboard and reporting applications. The endpoint supports all available
analytics metrics including conversation overviews, activity trends, label
usage, communication volumes, and detailed breakdowns, making it ideal for
creating unified analytics dashboards and comprehensive performance reports.

Authentication via API key is required to ensure secure access to workspace
data.

---

## Prerequisites

Ensure the following are in place:

### **1\. Generate Your API Key**

All APIs require a valid API key issued from your workspace. All requests must
include a valid API key in the request header (`X-API-Key`).

- Go to **Workspace → API Key** tab.

- Click **Add New Key** and check `Workspace Events Notification` as the scope.

- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

### **2\. Prepare Your Webhook Receiver**

Your server must:

- Be publicly accessible over **HTTPS**

- Accept **POST** requests

- Handle **application/json** payloads

---

## Endpoint

`POST https://seax.seasalt.ai/analytics-api/v1/generate_metric_report`

Use this endpoint to generate multiple analytics metrics in a single request,
providing a comprehensive view of your workspace performance across various
dimensions.

**Sample Request**

```bash
curl -X POST https://seax.seasalt.ai/analytics-api/v1/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["conversation_overview", "activity_trend"],
    "range_type": "last_30_days",
    "timezone": "America/Los_Angeles",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59"
  }'
```

### Request Fields

The request body uses the `AnalyticsRequestType` schema with the following
fields:

> **Note:** Fields marked with specific metric requirements are only used with
> certain metrics. See individual metric sections for detailed field
> dependencies.

| Field                    | Type                         | Required | Used By Metrics                             | Description                                            | Allowed Values / Example                                                                                                                                                                          |
| ------------------------ | ---------------------------- | -------- | ------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metrics`                | `array of strings`           | ✅       | All                                         | List of analytics metrics to generate                  | `["conversation_overview", "activity_trend", "label_usage", "conversation_breakdown", "communication_volume", "total_usage", "conversation_overview_yearly", "label_overview", "agent_activity"]` |
| `message_type`           | `string`                     |          | `activity_trend`                            | Whether to analyze messages or calls                   | `messages`, `calls`                                                                                                                                                                               |
| `time_unit`              | `string`                     |          | `activity_trend`, `label_usage`             | Aggregation level for time-based data                  | `day`, `month`, `year`                                                                                                                                                                            |
| `timezone`               | `string`                     |          | All time-based metrics                      | Timezone used for grouping and filtering               | Example: `UTC`, `Asia/Taipei`, `America/Los_Angeles` see a list of tz database time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)                                    |
| `start_date`             | `string (ISO 8601 datetime)` |          | Date range metrics (see individual metrics) | Custom start of the date range                         | Example: `2024-06-01T00:00:00` or `2024-06-01T23:59:59-07:00` (with timezone)                                                                                                                     |
| `end_date`               | `string (ISO 8601 datetime)` |          | Date range metrics (see individual metrics) | Custom end of the date range                           | Example: `2024-06-01T23:59:59` or `2024-06-01T23:59:59-07:00` (with timezone)                                                                                                                     |
| `range_type`             | `string`                     |          | `conversation_overview`, `agent_activity`   | Predefined time range (alternative to start/end dates) | `last_day`, `last_7_days`, `last_30_days`, `last_90_days`, `last_180_days`                                                                                                                        |
| `exclude_empty_response` | `boolean`                    |          | `conversation_overview`                     | Exclude conversations with no bot or agent replies     | `true`, `false`                                                                                                                                                                                   |
| `labels`                 | `array of strings`           |          | `label_usage`                               | Filter by specific label names                         | Example: `["support", "sales"]`                                                                                                                                                                   |
| `agents`                 | `array of strings`           |          | `agent_activity`                            | Filter by specific agent user accounts                 | Example: `["agent_user_1", "agent_user_2"]`                                                                                                                                                       |
| `year`                   | `string (YYYY)`              |          | `conversation_overview_yearly`              | Year for yearly report metrics                         | Example: `2024`                                                                                                                                                                                   |

### Metrics Use Case

| Metric                         | Compatible With         | Best Use Case                                |
| ------------------------------ | ----------------------- | -------------------------------------------- |
| `conversation_overview`        | Any metric              | Dashboard overview with other metrics        |
| `communication_volume`         | `conversation_overview` | Voice vs text communication analysis         |
| `activity_trend`               | `label_usage`           | Trend analysis with label patterns           |
| `label_overview`               | `label_usage`           | Label management and usage analysis          |
| `conversation_breakdown`       | `activity_trend`        | Detailed activity pattern analysis           |
| `total_usage`                  | Any metric              | High-level usage summaries                   |
| `conversation_overview_yearly` | Standalone recommended  | Annual reporting (resource intensive)        |
| `agent_activity`               | Any metric              | Agent availability and productivity tracking |

### Authorization

You must provide your API key in the `X-API-KEY` header.

To set up your API Key:

- Go to **Workspace → API Key** tab.
- Click **Add New Key** and check the `SeaX API Endpoints` scope.
- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

## Available Metrics

The following metrics are available through this endpoint. Each metric has
specific requirements and returns structured data:

> **Performance Tip:** Requesting multiple related metrics in a single call is
> more efficient than separate requests. However, avoid combining
> resource-intensive metrics like `conversation_overview_yearly` with others
> unless necessary.

### CONVERSATION_OVERVIEW

Provides comprehensive conversation statistics over a specified time range,
including message counts, user interactions, and percentage changes compared to
the previous period.

**Use Cases:**

- Dashboard overview widgets
- Comparing current vs previous period performance
- Monitoring agent workload and bot effectiveness

**Required Fields:**

- `metrics`: Must include `"conversation_overview"`
- `range_type`: Time range specification (use `last_30_days`, `last_7_days`,
  etc.)

**Optional Fields:**

- **`timezone`** (string): Timezone for date calculations and filtering

  - **Default:** `"UTC"`
  - **Example:** `"America/Los_Angeles"`, `"Asia/Tokyo"`, `"Europe/London"`
  - **Recommendation:** Set to your business timezone for accurate reporting

- **`exclude_empty_response`** (boolean): Filter out conversations with no bot
  or agent responses
  - **Default:** `false` (includes all conversations)
  - **Example:** `true` to focus only on engaged conversations
  - **Use case:** Set to `true` when analyzing actual engagement vs total
    traffic

> **Note:** This metric automatically calculates percentage changes by comparing
> with the equivalent previous period.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["conversation_overview"],
    "range_type": "last_30_days",
    "timezone": "America/Los_Angeles",
    "exclude_empty_response": true
  }'
```

**Sample Response:**

```json
{
  "conversation_overview": {
    "conversations": 150,
    "messages": 2500,
    "bot_messages": 1200,
    "agent_messages": 800,
    "live_agent_requests": 50,
    "distinct_user_count": 125,
    "conversations_change_percentage": 10.5,
    "messages_change_percentage": 5.0,
    "bot_messages_change_percentage": 8.0,
    "agent_messages_change_percentage": 12.0,
    "live_agent_requests_change_percentage": 15.0,
    "current_period_start": "2024-01-01T00:00:00Z",
    "current_period_end": "2024-01-31T23:59:59Z",
    "previous_period_start": "2023-12-01T00:00:00Z",
    "previous_period_end": "2023-12-31T23:59:59Z"
  }
}
```

### CONVERSATION_OVERVIEW_YEARLY

Provides yearly conversation statistics with monthly breakdown and average
calculations.

**Use Cases:**

- Annual performance reports
- Year-over-year analysis
- Monthly trend identification
- Resource planning based on historical data

**Required Fields:**

- `metrics`: Must include `"conversation_overview_yearly"`
- `year`: Year in YYYY format (e.g., `"2024"`)

**Optional Fields:**

- **`timezone`** (string): Timezone for date calculations
  - **Default:** `"UTC"`
  - **Example:** `"America/New_York"`, `"Europe/Berlin"`, `"Asia/Shanghai"`
  - **Note:** Affects how the year boundaries are calculated

> **Warning:** This is a resource-intensive metric. Avoid combining with
> multiple other metrics in high-frequency requests.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["conversation_overview_yearly"],
    "year": "2024",
    "timezone": "UTC"
  }'
```

**Sample Response:**

```json
{
  "conversation_overview_yearly": {
    "total_conversations": 1800,
    "total_messages": 15000,
    "average_messages_per_conversation": 8.33,
    "monthly_messages": {
      "January": 1200,
      "February": 1100,
      "March": 1300,
      "April": 1250,
      "May": 1400,
      "June": 1350,
      "July": 1450,
      "August": 1300,
      "September": 1200,
      "October": 1250,
      "November": 1100,
      "December": 1100
    }
  }
}
```

### CONVERSATION_BREAKDOWN

Provides detailed breakdown of conversation activity by channel, day of week,
and hour of day, useful for identifying peak activity periods and channel
preferences.

**Use Cases:**

- Staffing optimization (identify peak hours/days)
- Channel performance analysis
- Customer behavior pattern analysis
- Resource allocation planning

**Required Fields:**

- `metrics`: Must include `"conversation_breakdown"`
- `start_date`: Start of analysis period (ISO 8601 format)
- `end_date`: End of analysis period (ISO 8601 format)

**Optional Fields:**

- **`timezone`** (string): Timezone for hour-of-day and day-of-week analysis
  - **Default:** `"UTC"`
  - **Example:** `"America/Chicago"`, `"Asia/Seoul"`, `"Australia/Sydney"`
  - **Important:** Critical for accurate hour-of-day patterns as customer
    activity varies by local time
  - **Use case:** Set to your primary customer base timezone for meaningful
    staffing insights

> **Performance Tip:** Limit date ranges to 90 days or less for optimal
> performance.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["conversation_breakdown"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59",
    "timezone": "UTC"
  }'
```

**Sample Response:**

```json
{
  "conversation_breakdown": {
    "channel_summary": {
      "WebChat": {
        "user_count": 45,
        "inbound_message_count": 320,
        "outbound_message_count": 280,
        "total_message_count": 600
      },
      "SMS": {
        "user_count": 30,
        "inbound_message_count": 150,
        "outbound_message_count": 120,
        "total_message_count": 270
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
}
```

### LABEL_OVERVIEW

Returns comprehensive information about all labels in the workspace, including
usage counts and label metadata.

**Use Cases:**

- Label management and cleanup
- Understanding label usage patterns
- Contact segmentation analysis
- Label performance tracking

**Required Fields:**

- `metrics`: Must include `"label_overview"`

**Optional Fields:**

- None (this metric automatically returns all workspace labels including both
  custom and system labels)

> **Note:** This metric includes both custom and system labels. System labels
> may have `null` workspace_id.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["label_overview"]
  }'
```

**Sample Response:**

```json
{
  "label_overview": [
    {
      "id": "label-123",
      "name": "Support",
      "color": "#FF5733",
      "description": "Customer support inquiries",
      "total_count": 150,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T12:30:00Z"
    },
    {
      "id": "label-456",
      "name": "Sales",
      "color": "#33C3FF",
      "description": "Sales-related conversations",
      "total_count": 89,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-10T09:15:00Z"
    }
  ]
}
```

### COMMUNICATION_VOLUME

Provides counts of inbound/outbound voice calls and non-voice messages for a
specified time period.

**Use Cases:**

- Communication channel analysis
- Voice vs text usage tracking
- Capacity planning
- Service level monitoring

**Required Fields:**

- `metrics`: Must include `"communication_volume"`
- `start_date`: Start of analysis period (ISO 8601 format)
- `end_date`: End of analysis period (ISO 8601 format)

**Optional Fields:**

- **`timezone`** (string): Timezone for date range filtering
  - **Default:** `"UTC"`
  - **Example:** `"America/Denver"`, `"Europe/Paris"`, `"Asia/Mumbai"`
  - **Use case:** Ensures accurate date boundaries for your business operations

> **Note:** "Non-voice" includes SMS, chat messages, and other text-based
> communications.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["communication_volume"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59"
  }'
```

**Sample Response:**

```json
{
  "communication_volume": {
    "inbound_voice_count": 25,
    "outbound_voice_count": 15,
    "inbound_non_voice_count": 450
  }
}
```

### ACTIVITY_TREND

Tracks communication activity changes over time, with breakdowns by sender type
or call direction, including percentage change calculations.

**Use Cases:**

- Trend analysis over time
- Bot vs human agent performance tracking
- Seasonal pattern identification
- Growth/decline analysis

**Required Fields:**

- `metrics`: Must include `"activity_trend"`
- `start_date`: Start of analysis period (ISO 8601 format)
- `end_date`: End of analysis period (ISO 8601 format)

**Optional Fields:**

- **`message_type`** (string): Type of communication to analyze

  - **Default:** `"messages"`
  - **Options:**
    - `"messages"`: Shows breakdown by CUSTOMER/AGENT/BOT/SYSTEM sender types
    - `"calls"`: Shows breakdown by inbound/outbound call direction
  - **Example:** `"messages"` for chat analysis, `"calls"` for voice traffic
    analysis

- **`time_unit`** (string): Time period for data aggregation

  - **Default:** `"month"`
  - **Options:** `"day"`, `"month"`, `"year"`
  - **Example:** Use `"day"` for detailed short-term analysis, `"month"` for
    trend analysis
  - **Performance tip:** Use `"month"` or `"year"` for large date ranges

- **`timezone`** (string): Timezone for date grouping
  - **Default:** `"UTC"`
  - **Example:** `"America/Phoenix"`, `"Europe/Rome"`, `"Asia/Bangkok"`
  - **Use case:** Ensures trend periods align with your business calendar

> **Performance Tip:** Use `"month"` or `"year"` time_unit for large date ranges
> to reduce response size.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["activity_trend"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59",
    "message_type": "messages",
    "time_unit": "day"
  }'
```

**Sample Response:**

```json
{
  "activity_trend": {
    "time_unit": "day",
    "data": [
      {
        "period": "2024-01-01",
        "CUSTOMER": 45,
        "AGENT": 60,
        "BOT": 20,
        "SYSTEM": 5
      },
      {
        "period": "2024-01-02",
        "CUSTOMER": 50,
        "AGENT": 70,
        "BOT": 25,
        "SYSTEM": 3
      }
    ],
    "change_percent": 12.5
  }
}
```

### LABEL_USAGE

Returns label usage statistics over time, grouped by the specified time unit.

**Use Cases:**

- Label trend analysis
- Campaign effectiveness tracking
- Seasonal label usage patterns
- Specific label performance monitoring

**Required Fields:**

- `metrics`: Must include `"label_usage"`
- `start_date`: Start of analysis period (ISO 8601 format)
- `end_date`: End of analysis period (ISO 8601 format)

**Optional Fields:**

- **`time_unit`** (string): Time period for data grouping

  - **Default:** `"month"`
  - **Options:** `"day"`, `"month"`, `"year"`
  - **Example:** `"day"` for daily label application patterns, `"month"` for
    monthly trends
  - **Use case:** Choose based on your analysis timeframe and data volume

- **`labels`** (array of strings): Specific label names to include in analysis

  - **Default:** Returns data for all available labels in the workspace
  - **Example:** `["support", "sales", "billing"]` to focus on key business
    categories
  - **Performance tip:** Filter to specific labels to reduce response size and
    focus analysis
  - **Use case:** Monitor specific campaign labels or department categories

- **`timezone`** (string): Timezone for time period boundaries
  - **Default:** `"UTC"`
  - **Example:** `"America/Los_Angeles"`, `"Europe/London"`, `"Asia/Tokyo"`
  - **Use case:** Align time periods with your business calendar for accurate
    trend analysis

> **Tip:** Use the `labels` filter to focus on specific labels of interest and
> reduce response size.

**Sample Request:**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["label_usage"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-02-29T23:59:59",
    "time_unit": "month",
    "labels": ["support", "sales", "billing"]
  }'
```

**Sample Response:**

```json
{
  "label_usage": [
    {
      "period": "2024-01",
      "labels": [
        { "name": "support", "count": 45 },
        { "name": "sales", "count": 32 },
        { "name": "billing", "count": 18 }
      ]
    },
    {
      "period": "2024-02",
      "labels": [
        { "name": "support", "count": 52 },
        { "name": "sales", "count": 28 },
        { "name": "billing", "count": 22 }
      ]
    }
  ]
}
```

### TOTAL_USAGE

Returns summary of total voice call duration and chat message counts over a
specified period.

**Use Cases:**

- Billing and usage tracking
- Resource consumption monitoring
- Service usage summaries
- Cost analysis

**Required Fields:**

- `metrics`: Must include `"total_usage"`

**Optional Fields:**

- **`start_date`** (string, ISO 8601 datetime): Beginning of the analysis period

  - **Default:** If omitted, uses all available historical data from the
    beginning of records
  - **Example:** `"2024-01-01T00:00:00"`, `"2024-06-15T00:00:00-07:00"`
  - **Use case:** Specify to analyze usage for a particular period, or omit for
    total lifetime usage

- **`end_date`** (string, ISO 8601 datetime): End of the analysis period

  - **Default:** If omitted, uses all available data up to the current time
  - **Example:** `"2024-12-31T23:59:59"`, `"2024-06-30T23:59:59+08:00"`
  - **Use case:** Specify for period analysis, or omit for usage up to now

- **`timezone`** (string): Timezone for date range interpretation
  - **Default:** `"UTC"`
  - **Example:** `"America/New_York"`, `"Europe/Amsterdam"`, `"Asia/Singapore"`
  - **Use case:** Ensures date boundaries match your business timezone

> **Note:** If no date range is specified, returns total usage across all
> available data.

**Sample Request:**

```bash
curl -X POST https://your-seax-domain.com/api/v1/analytics/generate_metric_report \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["total_usage"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59"
  }'
```

**Sample Response:**

```json
{
  "total_usage": {
    "total_voice_minutes": 450.5,
    "total_chat_responses": 2500
  }
}
```

### AGENT_ACTIVITY

Provides detailed agent activity data including online/offline status sessions
with timestamps and duration, enabling workforce management and productivity
analysis.

**Use Cases:**

- Agent availability tracking
- Workforce scheduling optimization
- Productivity analysis and reporting
- Agent performance monitoring
- Shift coverage analysis

**Required Fields:**

- `metrics`: Must include `"agent_activity"`
- Either `range_type` OR both `start_date` and `end_date`

**Optional Fields:**

- **`agents`** (array of strings): List of specific agent user accounts to
  filter by

  - **Default:** If omitted, returns data for all agents in the workspace
  - **Example:**
    `["agent_user_1@email.com", "agent_user_2@email.com", "agent_user_3@email.com"]`
  - **Use case:** Monitor specific team members or department agents
  - **Performance tip:** Filter to specific agents to reduce response size when
    analyzing individual performance

- **`timezone`** (string): Timezone for date range interpretation
  - **Default:** `"UTC"`
  - **Example:** `"America/Chicago"`, `"Europe/Madrid"`, `"Asia/Hong_Kong"`
  - **Use case:** Align activity timestamps with your business timezone for
    accurate shift analysis

> **Note:** Activity sessions include status, start time, end time, and duration
> in seconds.

#### Available Agent Status Values

The `status` field in the response can have the following values:

| Status           | Description                                        |
| ---------------- | -------------------------------------------------- |
| `AVAILABLE`      | Agent is online and ready to handle conversations  |
| `OFFLINE`        | Agent is not logged in or has gone offline         |
| `ON_THE_CALL`    | Agent is currently handling a voice call           |
| `CALL_RINGING`   | An incoming call is ringing for the agent          |
| `OUTBOUND`       | Agent is making an outbound call                   |
| `WRAP_UP`        | Agent is in post-call wrap-up time                 |
| `MEAL`           | Agent is on a meal break                           |
| `BREAK`          | Agent is on a regular break                        |
| `AWAY`           | (Deprecated) Agent is temporarily away             |
| `DO_NOT_DISTURB` | (Deprecated) Agent has enabled do-not-disturb mode |

> **Important:** The `AWAY` and `DO_NOT_DISTURB` statuses are deprecated but may
> appear in historical data for backward compatibility.

**Sample Request with Range Type:**

```bash
curl -X POST https://seax.seasalt.ai/analytics-api/v1/generate_metric_report \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["agent_activity"],
    "range_type": "last_7_days",
    "agents": ["agent_user_1", "agent_user_2"],
    "timezone": "America/Los_Angeles"
  }'
```

**Sample Request with Date Range:**

```bash
curl -X POST https://seax.seasalt.ai/analytics-api/v1/generate_metric_report \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["agent_activity"],
    "start_date": "2024-01-15T00:00:00",
    "end_date": "2024-01-15T23:59:59",
    "timezone": "UTC"
  }'
```

**Sample Response:**

```json
{
  "agent_activity": {
    "agents": [
      {
        "agent_id": "agent_user_1",
        "status": "AVAILABLE",
        "start_time": "2024-01-15T08:00:00Z",
        "end_time": "2024-01-15T10:30:00Z",
        "duration_seconds": 9000
      },
      {
        "agent_id": "agent_user_1",
        "status": "ON_THE_CALL",
        "start_time": "2024-01-15T10:30:00Z",
        "end_time": "2024-01-15T11:00:00Z",
        "duration_seconds": 1800
      },
      {
        "agent_id": "agent_user_1",
        "status": "WRAP_UP",
        "start_time": "2024-01-15T11:00:00Z",
        "end_time": "2024-01-15T11:05:00Z",
        "duration_seconds": 300
      },
      {
        "agent_id": "agent_user_1",
        "status": "MEAL",
        "start_time": "2024-01-15T12:00:00Z",
        "end_time": "2024-01-15T13:00:00Z",
        "duration_seconds": 3600
      },
      {
        "agent_id": "agent_user_1",
        "status": "AVAILABLE",
        "start_time": "2024-01-15T13:00:00Z",
        "end_time": "2024-01-15T17:00:00Z",
        "duration_seconds": 14400
      },
      {
        "agent_id": "agent_user_2",
        "status": "AVAILABLE",
        "start_time": "2024-01-15T09:00:00Z",
        "end_time": "2024-01-15T15:00:00Z",
        "duration_seconds": 21600
      },
      {
        "agent_id": "agent_user_2",
        "status": "BREAK",
        "start_time": "2024-01-15T15:00:00Z",
        "end_time": "2024-01-15T15:15:00Z",
        "duration_seconds": 900
      },
      {
        "agent_id": "agent_user_2",
        "status": "OFFLINE",
        "start_time": "2024-01-15T17:00:00Z",
        "end_time": null,
        "duration_seconds": null
      }
    ]
  }
}
```

## Complete Sample Request and Response

**Sample Request with Multiple Metrics:**

```bash
curl -X POST https://your-seax-domain.com/api/v1/analytics/generate_metric_report \
  -H "X-API-KEY: <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": [
      "conversation_overview",
      "communication_volume",
      "label_overview"
    ],
    "range_type": "last_30_days",
    "timezone": "America/Los_Angeles",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59"
  }'
```

**Sample Successful Response:**

```json
{
  "conversation_overview": {
    "conversations": 150,
    "messages": 2500,
    "bot_messages": 1200,
    "agent_messages": 800,
    "live_agent_requests": 50,
    "distinct_user_count": 125,
    "conversations_change_percentage": 10.5,
    "messages_change_percentage": 5.0,
    "bot_messages_change_percentage": 8.0,
    "agent_messages_change_percentage": 12.0,
    "live_agent_requests_change_percentage": 15.0,
    "current_period_start": "2024-01-01T00:00:00Z",
    "current_period_end": "2024-01-31T23:59:59Z",
    "previous_period_start": "2023-12-01T00:00:00Z",
    "previous_period_end": "2023-12-31T23:59:59Z"
  },
  "communication_volume": {
    "inbound_voice_count": 25,
    "outbound_voice_count": 15,
    "inbound_non_voice_count": 450
  },
  "label_overview": [
    {
      "id": "label-123",
      "name": "Support",
      "color": "#FF5733",
      "description": "Customer support inquiries",
      "total_count": 150,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T12:30:00Z"
    },
    {
      "id": "label-456",
      "name": "Sales",
      "color": "#33C3FF",
      "description": "Sales-related conversations",
      "total_count": 89,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-10T09:15:00Z"
    }
  ]
}
```

## Error Responses

The API returns specific error messages to help you troubleshoot issues:

**400 Bad Request - Missing Required Field:**

```json
{
  "detail": "Range type is required for conversation overview"
}
```

_Solution: Add the `range_type` field when using the `conversation_overview`
metric._

**400 Bad Request - Invalid Metric:**

```json
{
  "detail": "Unsupported metric: invalid_metric_name"
}
```

_Solution: Check the metric name against the supported list in the schema table
above._

**400 Bad Request - Date Range Required:**

```json
{
  "detail": "Start date and end date are required for conversation breakdown"
}
```

_Solution: Provide both `start_date` and `end_date` fields for date-range
metrics._

**401 Unauthorized:**

```json
{
  "detail": "Invalid API key"
}
```

_Solution: Verify your API key is correct and has the appropriate permissions._

**422 Validation Error:**

```json
{
  "detail": [
    {
      "loc": ["body", "metrics"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

_Solution: Ensure all required fields are included in your request body._

## Common Error Scenarios

| Error                                  | Cause                                | Solution                                 |
| -------------------------------------- | ------------------------------------ | ---------------------------------------- |
| "Range type is required"               | Missing `range_type` for overview    | Add `range_type` field                   |
| "Year is required"                     | Missing `year` for yearly overview   | Add `year` field in YYYY format          |
| "Start date and end date are required" | Missing dates for time-range metrics | Add both `start_date` and `end_date`     |
| "Invalid year format"                  | Incorrect year format                | Use 4-digit year format (e.g., "2024")   |
| "Unsupported metric"                   | Typo in metric name                  | Check spelling against supported metrics |

#### Best Practices

##### Request Optimization

1. **Batch Related Metrics**: Request related metrics together to minimize API
   calls and ensure data consistency.

   - ✅ Good: `["conversation_overview", "communication_volume"]`
   - ❌ Avoid: Separate calls for each metric

2. **Timezone Consistency**: Always specify the same timezone across related
   requests to ensure accurate comparisons.

   - ✅ Good: Set `"timezone": "America/Los_Angeles"` for all requests
   - ❌ Avoid: Mixing UTC and local timezones in related queries

3. **Date Range Optimization**:
   - Use `range_type` for standard periods instead of custom dates when possible
   - Limit date ranges to 90 days or less for complex metrics
   - Ensure `start_date` is before `end_date`

##### Error Handling

4. **Comprehensive Error Handling**: Implement proper error handling for each
   metric, as some may succeed while others fail due to missing required fields.
   ```javascript
   // Example error handling
   try {
     const response = await fetch('/api/v1/analytics/generate_metric_report', {
       method: 'POST',
       headers: { 'X-API-KEY': apiKey, 'Content-Type': 'application/json' },
       body: JSON.stringify(requestBody),
     });
     if (!response.ok) {
       const error = await response.json();
       console.error('API Error:', error.detail);
     }
   } catch (error) {
     console.error('Network Error:', error);
   }
   ```

##### Performance Optimization

5. **Query Performance**:

   - Avoid `conversation_overview_yearly` in high-frequency requests
   - Use appropriate `time_unit` values (prefer `month` over `day` for large
     ranges)
   - Consider implementing client-side caching for frequently requested
     combinations
   - Set reasonable request timeouts (30-60 seconds for complex queries)

6. **Resource Management**:
   - Don't request more metrics than needed for your use case
   - Use label filtering (`labels` parameter) to reduce response size
   - Monitor API quota usage for high-volume applications

##### Data Consistency

7. **Timezone Handling**:

   - Always specify timezone for business reporting
   - Use the same timezone across related dashboard widgets
   - Consider user's local timezone for UI display

8. **Date Range Logic**:
   - Validate date ranges on the client side before API calls
   - Handle edge cases like month boundaries and leap years
   - Consider business calendar vs calendar dates for reporting

## Real-World Usage Examples

**Dashboard Overview (Most Common)**

```bash
curl -X POST https://seax.seasalt.ai/seax-api/api/v1/analytics/generate_metric_report
ric_report
  -H "X-API-KEY: your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["conversation_overview", "communication_volume"],
    "range_type": "last_30_days",
    "timezone": "America/New_York"
  }'
```

**Detailed Analysis**

```bash
curl -X POST https://api.example.com/v1/analytics/generate_metric_report \
  -H "X-API-KEY: your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["activity_trend", "conversation_breakdown"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59",
    "time_unit": "day",
    "timezone": "UTC"
  }'
```

**Label Performance Review**

```bash
curl -X POST https://api.example.com/v1/analytics/generate_metric_report \
  -H "X-API-KEY: your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": ["label_overview", "label_usage"],
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59",
    "labels": ["support", "sales", "billing"]
  }'
```
