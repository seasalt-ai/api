---
title: Portal API Wiki
linkTitle: Portal API
type: docs
menu: {main: {weight: 40}}
---



## Overview
Welcome to the **Portal API Wiki**. This site serves as the central hub for all developer documentation related to the Seasalt.ai Portal system.

Whether you're just getting started or looking to integrate advanced features, this documentation will guide you through everything you need to know.

## Key Features
Currently supported core features include:

- **Webhook**: Receive real-time event notifications from the Seasalt.ai, enabling instant updates and seamless system integration.
- **Analytics**: Access insights and usage metrics to help you monitor activity and make data-driven decisions.


## Prerequisites

Before you can interact with the Portal APIs, ensure the following are in
place:

### **1\. A Seasuite Portal Account**

Sign up or log into your [Seasuite Portal](https://portal.seasalt.ai/).

### **2\. Generate Your API Key**

All APIs require a valid API key issued from your workspace. All requests must include a valid API key in the request header (`X-API-Key`).

- Go to **Settings → API Key** tab.

- Click **Add New Key**.

- Copy the key and keep it safe. This key is required in the `X-API-KEY` header
  for **all requests**.

#### Sample Request

```javascript
curl -X GET "https://portal.seasalt.ai/notify/api/v1/workspaces/{workspace_id}/logs/{subscription_id}?event_type=conversation.new&delivery_status=success&order_by=created_at:desc&limit=10&offset=0" \
  -H "X-API-KEY: <your_api_key>"

```

## Getting Started
We recommend starting with this page for a high-level overview. You can then explore each feature module in detail through the sidebar navigation.
