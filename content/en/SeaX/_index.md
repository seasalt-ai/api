---
title: SeaX API Wiki
linkTitle: SeaX API
type: docs
menu: {main: {weight: 20}}
---

## Overview

SeaX Bulk SMS API provides comprehensive SMS/MMS communication management capabilities designed to help businesses effectively manage customer communications through text messaging. This powerful platform enables organizations to send bulk messages, manage contact databases, execute sophisticated campaigns, and handle both inbound and outbound communications with advanced automation and analytics capabilities.

The SeaX platform is built to scale with your business needs, whether you're sending a few hundred messages per month or managing millions of communications across multiple campaigns. The API provides robust features for compliance management, delivery tracking, and customer engagement optimization, making it an ideal solution for businesses of all sizes that rely on SMS/MMS communications.

With SeaX Bulk SMS API, you can create sophisticated messaging workflows that respect customer preferences, comply with regulatory requirements, and deliver measurable results. The platform supports advanced features like scheduled messaging, keyword-based auto-responses, contact segmentation, and comprehensive analytics to help you optimize your messaging strategies.

## Key Features

### Sending Capabilities

#### Bulk SMS/MMS Messaging
SeaX excels at handling large-scale messaging operations, allowing you to send thousands or millions of SMS and MMS messages efficiently. The bulk messaging system is designed to handle high-volume campaigns while maintaining delivery reliability and speed.

The platform supports both SMS (text-only) and MMS (multimedia) messages, enabling you to send rich content including images, videos, and other media files. This multimedia capability allows for more engaging customer communications and higher response rates compared to text-only messaging.

The bulk messaging system includes intelligent queuing and throttling mechanisms to ensure optimal delivery rates while respecting carrier limitations and maintaining good sender reputation. Messages are processed through multiple carrier networks to ensure maximum deliverability and redundancy.

#### Scheduled Messaging
One of the most powerful features of SeaX is its ability to schedule messages up to 7 days in advance. This scheduling capability enables you to plan and execute time-sensitive campaigns, send messages at optimal times for your audience, and automate recurring communications.

The scheduling system takes into account time zones, business hours, and customer preferences to optimize message delivery timing. You can schedule individual messages or entire campaigns, and the system provides confirmation and status updates as scheduled messages are processed.

Advanced scheduling features include the ability to modify or cancel scheduled messages before they're sent, bulk scheduling operations, and integration with external calendar systems for complex campaign coordination.

#### Bulk Voice Drops
SeaX makes it easy to deliver pre-recorded voice messages to large groups of contacts with just a few clicks. This powerful feature is ideal for announcements, reminders, emergency alerts, or any campaign where a personal touch via voice is more effective than text.

With bulk voice drops, you can upload your audio, select your audience, and send out thousands of voice messages in a highly scalable and efficient way. The system handles call distribution automatically, ensuring high deliverability and minimal manual effort.

#### AI Agent Campaigns
SeaX empowers you to connect your customers with AI agents you've tailored to your business. SeaX makes it easy to place bulk call campaigns that drive real-time, automated conversations.

Customers can speak freely with your automated agents through natural, two-way voice conversations. perfect for lead qualification, appointment scheduling, surveys, and more.

#### Do Not Contact Compliance
SeaX automatically respects "Do Not Contact" (DNC) preferences and maintains comprehensive opt-out management. The system automatically processes standard opt-out keywords like "STOP," "UNSUBSCRIBE," and "REMOVE ME," ensuring compliance with telecommunications regulations and customer preferences.

The DNC management system maintains a centralized database of opt-out preferences that's automatically consulted before any message is sent. This prevents accidental messaging to customers who have opted out and helps maintain compliance with regulations like TCPA and CAN-SPAM.

Customers can opt back in through various mechanisms, and the system maintains a complete audit trail of all opt-in and opt-out activities for compliance reporting and customer service purposes.

#### Delivery Reports and Analytics
Comprehensive delivery reporting provides detailed insights into message performance, delivery rates, and customer engagement. The system tracks messages through the entire delivery pipeline, providing real-time status updates and detailed analytics.

Delivery reports include information about successful deliveries, failed attempts, bounce reasons, and carrier-specific delivery data. This information is crucial for optimizing message content, timing, and targeting to improve overall campaign performance.

Advanced analytics features include delivery rate trending, carrier performance analysis, and customer engagement metrics that help you understand how your messaging campaigns are performing and where improvements can be made.

#### Multi-number Support
SeaX supports sending messages from multiple phone numbers, enabling you to scale your messaging operations and maintain separate numbers for different types of communications or business units. This multi-number capability also provides redundancy and helps distribute messaging load across multiple carrier connections.

You can assign specific phone numbers to different campaigns, customer segments, or message types, allowing for better organization and tracking of your messaging activities. The system automatically manages number rotation and load balancing to optimize delivery performance.

### Receiving Capabilities

#### Auto Opt-in and Opt-out Processing
The platform automatically captures and processes opt-in and opt-out requests from customers, maintaining compliance with regulatory requirements while providing a seamless experience for customers who want to manage their communication preferences.

The auto opt-in system can process various types of opt-in requests, including keyword-based opt-ins, web form submissions, and API-driven opt-ins from other systems. All opt-in activities are logged with timestamps and source information for compliance auditing.

The opt-out processing system recognizes standard opt-out keywords and phrases, automatically updating customer preferences and sending confirmation messages as required by regulations. The system also supports custom opt-out keywords and can be configured to handle industry-specific opt-out requirements.

#### Reply Handling and Customer Engagement
SeaX provides sophisticated reply handling capabilities that enable two-way conversations with customers. The system can automatically route replies to appropriate handlers, trigger automated responses, or forward messages to human operators for personal attention.

The reply handling system maintains conversation context and can trigger different actions based on message content, customer history, and predefined rules. This enables sophisticated customer service workflows and automated support scenarios.

Advanced reply handling features include sentiment analysis, automatic escalation for urgent issues, and integration with CRM systems to provide complete customer interaction history.

#### Keyword Matching and Auto-responses
The platform includes a powerful keyword matching engine that can automatically respond to customer messages based on predefined keywords and phrases. This automation capability enables 24/7 customer support and instant responses to common inquiries.

The keyword matching system supports exact matches, partial matches, and fuzzy matching to handle variations in customer language and spelling. You can configure different response actions for different keywords, including sending automated replies, adding customer labels, or triggering external system integrations.

Advanced keyword features include support for multiple languages, context-aware matching, and machine learning-enhanced keyword recognition that improves over time based on customer interactions.

### Contact Management

#### Import and Export Capabilities
SeaX provides robust contact management features including bulk import and export capabilities that support various file formats including CSV, Excel, and custom formats. The import system can handle large contact lists with millions of records while maintaining data integrity and validation.

The import process includes data validation, duplicate detection, and error reporting to ensure that your contact database remains clean and accurate. You can map import fields to custom contact attributes and apply transformation rules during the import process.

Export capabilities enable you to extract contact data for analysis, backup, or integration with other systems. Exports can be filtered by various criteria and scheduled to run automatically at regular intervals.

#### Labeling and Segmentation System
The platform includes a sophisticated labeling system that allows you to assign multiple labels to contacts for organization, segmentation, and targeting purposes. Labels can be applied manually, automatically based on customer behavior, or through API integrations with other systems.

The labeling system supports hierarchical labels, custom label attributes, and dynamic labeling based on customer interactions and preferences. This enables sophisticated customer segmentation and personalized messaging strategies.

Advanced segmentation features include the ability to create complex label combinations, time-based label expiration, and automatic label assignment based on customer lifecycle stages or engagement patterns.

#### Group Messaging and Targeting
With the labeling system in place, you can easily send targeted messages to specific customer segments by selecting contacts based on their labels. This targeting capability enables personalized messaging campaigns that are more relevant and effective than broad, untargeted communications.

The group messaging system supports complex targeting criteria including label combinations, geographic filters, and behavioral triggers. You can create reusable audience segments and apply them to multiple campaigns for consistent targeting.

Advanced targeting features include A/B testing capabilities, dynamic audience updates, and integration with external data sources for enhanced customer profiling and targeting accuracy.

## Getting Started

### Authentication Options

SeaX Bulk SMS API provides two primary authentication methods to accommodate different integration scenarios and security requirements.

#### Access Token Authentication
Access tokens provide short-lived authentication credentials that are ideal for interactive applications and scenarios where token refresh capabilities are available. Access tokens have a limited lifetime for security purposes and must be refreshed periodically using refresh tokens.

To obtain an access token, you must first authenticate with SeaAuth using the scope `seax-bulk-sms`. This scope specifically authorizes the access token to use SeaX Bulk SMS API endpoints. The authentication process returns both an access token and a refresh token that can be used to obtain new access tokens when the current one expires.

Access tokens should be included in the Authorization header of API requests using the Bearer token format: `Authorization: Bearer [access-token]`. This method is recommended for applications that can handle token refresh logic and need the enhanced security of short-lived credentials.

#### API Key Authentication (Recommended)
API keys provide long-lived authentication credentials that are more convenient for backend integrations and automated systems. Unlike access tokens, API keys don't expire automatically, making them ideal for server-to-server communications and batch processing scenarios.

To create an API key, use the `POST /api/v1/workspace/{workspace_id}/api_keys/reset` endpoint. This will generate a new API key and invalidate any existing keys for security purposes. API keys should be stored securely and treated as sensitive credentials.

API keys are included in requests using the `X-API-Key` header: `X-API-Key: [your-api-key]`. This method is recommended for most integration scenarios due to its simplicity and reliability.

### Quick Start Guide

#### Sending a Campaign

The campaign workflow is designed to handle bulk messaging operations efficiently while providing comprehensive tracking and management capabilities.

**Step 1: Generate API Key**
Begin by creating an API key for authentication. This key will be used for all subsequent API calls and should be stored securely in your application configuration.

```bash
curl -X POST \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/{workspace_id}/api_keys/reset' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer [access-token]' \
  -d '{"name": "My Integration API Key"}'
```

**Step 2: Import Contacts**
Upload your contact list using either the CSV import endpoint or individual contact creation endpoints. The import process is asynchronous for large contact lists.

```bash
curl -X POST \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/{workspace_id}/import_contacts' \
  -H 'X-API-Key: [your-api-key]' \
  -F 'file=@contacts.csv' \
  -F 'label_ids=["label1", "label2"]'
```

**Step 3: Monitor Import Progress**
Use the job ID returned from the import request to monitor progress. The import is complete when the job status is either "finished" or "failed."

```bash
curl -X GET \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/{workspace_id}/jobs/{job_id}' \
  -H 'X-API-Key: [your-api-key]'
```

**Step 4: Create and Launch Campaign**
Once contacts are imported, create a campaign specifying the message content, target audience, and scheduling parameters.

```bash
curl -X POST \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/{workspace_id}/campaigns' \
  -H 'X-API-Key: [your-api-key]' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Welcome Campaign",
    "type": "SMS",
    "message": "Welcome to our service!",
    "phone_number": "+1234567890",
    "contact_label_ids": ["new_customers"]
  }'
```

**Step 5: Monitor Campaign Execution**
Track campaign progress using the job ID returned from campaign creation. Monitor delivery rates and customer responses through the campaign logs endpoint.

#### Sending Individual Messages

For immediate, individual message sending, the process is more straightforward and doesn't require campaign setup.

**Step 1: Get Sender Phone Numbers**
Retrieve the list of available phone numbers that can be used for sending messages.

```bash
curl -X GET \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/{workspace_id}/phones' \
  -H 'X-API-Key: [your-api-key]'
```

**Step 2: Send Message**
Send an SMS or MMS message directly to a specific recipient using one of your available phone numbers.

```bash
curl -X POST \
  'https://seax.seasalt.ai/bulk-sms-api/api/v1/workspace/{workspace_id}/send_message' \
  -H 'X-API-Key: [your-api-key]' \
  -H 'Content-Type: application/json' \
  -d '{
    "phone_number": "+1234567890",
    "to_phone_number": "+0987654321",
    "content": "Hello! This is a test message.",
    "media_urls": ["https://example.com/image.jpg"]
  }'
```

## Core Workflows

### Campaign Management

Campaign management in SeaX involves creating, configuring, executing, and monitoring bulk messaging operations. The campaign system is designed to handle complex messaging scenarios while providing detailed tracking and analytics.

#### Campaign Creation and Configuration
When creating a campaign, you specify the campaign type (SMS, MMS, AI_AGENT, or WHATSAPP_BUSINESS_PLATFORM_MESSAGE), target audience, message content, and scheduling parameters. The campaign configuration determines how messages will be sent and to whom.

Campaign configuration includes options for message personalization, delivery timing, and response handling. You can configure campaigns to run immediately or schedule them for future execution, and you can specify complex targeting criteria based on contact labels and attributes.

Advanced campaign features include A/B testing capabilities, message personalization using contact attributes, and integration with external systems for dynamic content generation.

#### Campaign Execution and Monitoring
Once a campaign is launched, t
(Content truncated due to size limit. Use line ranges to read in chunks)

{{% pageinfo %}}
This is a placeholder page that shows you how to use this template site.
{{% /pageinfo %}}

This section is where the user documentation for your project lives - all the
information your users need to understand and successfully use your project.

For large documentation sets we recommend adding content under the headings in
this section, though if some or all of them don’t apply to your project feel
free to remove them or add your own. You can see an example of a smaller Docsy
documentation site in the [Docsy User Guide](https://docsy.dev/docs/), which
lives in the [Docsy theme
repo](https://github.com/google/docsy/tree/master/userguide) if you'd like to
copy its docs section.

Other content such as marketing material, case studies, and community updates
should live in the [About](/about/) and [Community](/community/) pages.

Find out how to use the Docsy theme in the [Docsy User
Guide](https://docsy.dev/docs/). You can learn more about how to organize your
documentation (and how we organized this site) in [Organizing Your
Content](https://docsy.dev/docs/best-practices/organizing-content/).
