---
title: Portal API Wiki
linkTitle: Portal API
type: docs
description:
  Complete reference for Seasalt.ai Portal APIs, including webhook, analytics,
  subscription management, and integration endpoints for building custom
  workflows.
menu: { main: { weight: 40 } }
---

## Overview

Welcome to the **Portal API Wiki**. This site serves as the central hub for all
developer documentation related to the Seasalt.ai Portal system. The Portal API
provides secure access to workspace-level data, enabling you to retrieve
analytics and usage information for reporting and insights and set up event
webhook subscriptions.

Whether you're just getting started or looking to integrate advanced features,
this documentation will guide you through everything you need to know.

## Key Features

Currently supported core features include:

- **Webhook Notifications**: Receive real-time event notifications from the
  Seasalt.ai, enabling instant updates and seamless system integration.
- **Analytics**: Access insights and usage metrics to help you monitor activity
  and make data-driven decisions

You can also access the RESTful API docs here:

- Webhook Notifications: https://portal.seasalt.ai/notify/redoc
- Analytics: https://portal.seasalt.ai/portal-api/redoc

## Prerequisites

Before you can interact with the Portal APIs, ensure the following are in place:

### **1\. A Seasalt.ai Portal Account**

Sign up or log into your [Seasuite Portal](https://portal.seasalt.ai/).

### **2\. Generate Your API Key**

All APIs require a valid API key issued from your workspace. All requests must
include a valid API key in the request header (`X-API-Key`). Please select just
enough scope you’ll need for your purpose. Refer to corresponding section to see
the API key scope requirements.

- [Webhook Notifications](./Webhook.md/#1-generate-your-api-key)
- [Analytics](./Analytics.md/#authorization)

#### Sample Request

```javascript
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/{subscription_id}?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

## Getting Started

We recommend starting with this page for a high-level overview. You can then
explore each feature module in detail through the sidebar navigation.
