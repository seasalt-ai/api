---
title: Refeactored SeaX Multi-Channel Messaging API Wiki (Refactored)
linkTitle: Refeactored SeaX API
type: docs
weight: 2
---

## Overview

The SeaX Multi-Channel Messaging API is a comprehensive communication platform that enables businesses to integrate and automate messaging across SMS, WhatsApp, and voice channels. Built for scalability and enterprise use, SeaX provides unified tools for multi-channel campaigns, contact management, and conversational workflows across all major messaging platforms.

## Supported Channels

### 📱 SMS & MMS Messaging
- **Bulk SMS Campaigns**: Send text messages to large contact lists
- **MMS Support**: Share images, videos, and rich media content  
- **Two-Way Messaging**: Receive replies and engage in SMS conversations
- **Delivery Reports**: Track message delivery status and engagement

### 💬 WhatsApp Business Platform
- **Rich Media Messages**: Send images, documents, videos, and audio
- **Template Messages**: Use pre-approved templates for notifications
- **Interactive Messages**: Buttons, lists, and quick reply options
- **Business API Compliance**: Full WhatsApp Business API integration
- **Highly Structured Messages (HSM)**: Certified template messaging

### 📞 Voice & Phone Calls  
- **Auto Dialer Campaigns**: Automated outbound call campaigns
- **Custom Call Scripts**: Dynamic call flows and interactions
- **Interactive Voice Response (IVR)**: Menu-driven call handling
- **Call Recording**: Record and analyze call interactions
- **Callback Management**: Handle inbound calls and callbacks

## Key Features

- **Unified Contact Management**: Manage contacts across all channels from one platform
- **Multi-Channel Campaigns**: Coordinate messaging across SMS, WhatsApp, and voice
- **Advanced Analytics**: Track performance metrics across all channels
- **Webhook Integrations**: Real-time notifications for all channel events
- **Template Management**: Consistent messaging templates across channels
- **Conversation Threading**: Unified conversation views across channels

## Authentication

SeaX API uses API key authentication. To obtain your API key:

1. Log into your SeaX account
2. Navigate to the "Settings" tab
3. Generate your API key in the API Access section
4. Use the key in your request headers

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/campaigns
```

## Base URL

All API requests should be made to:
```
https://seax.seasalt.ai/api/v1/
```

## Channel-Specific Implementation

### SMS & MMS Messaging

#### Sending a Single SMS
```javascript
const response = await fetch('https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/send_message', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    to: '+1234567890',
    from: '+1987654321',
    body: 'Hello! This is a test message from SeaX.',
    message_type: 'sms'
  })
});

const result = await response.json();
console.log('Message sent:', result.message_id);
```

#### Bulk SMS Campaign
```python
import requests

url = "https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/campaigns"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

campaign_data = {
    "name": "Spring Sale Campaign",
    "message": "🌸 Spring Sale! Get 20% off all items. Use code SPRING20. Shop now!",
    "from_number": "+1987654321",
    "contacts": [
        "+1234567890",
        "+1234567891", 
        "+1234567892"
    ],
    "schedule_time": "2024-04-01T10:00:00Z",
    "campaign_type": "sms"
}

response = requests.post(url, headers=headers, json=campaign_data)
print(f"SMS Campaign created: {response.json()}")
```

#### Sending MMS with Media
```javascript
const mmsResponse = await fetch('https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/send_message', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    to: '+1234567890',
    from: '+1987654321',
    body: 'Check out our new product!',
    media_url: 'https://example.com/product-image.jpg',
    message_type: 'mms'
  })
});
```

### WhatsApp Business Platform

#### Send WhatsApp Template Message
```python
whatsapp_template = {
    "to": "+1234567890",
    "template_name": "order_confirmation",
    "template_language": "en_US",
    "components": [
        {
            "type": "body",
            "parameters": [
                {
                    "type": "text",
                    "text": "John Doe"
                },
                {
                    "type": "text", 
                    "text": "ORD-12345"
                }
            ]
        }
    ]
}

response = requests.post(
    "https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/send_message/wabp_template_message",
    headers=headers,
    json=whatsapp_template
)
```

#### Send Interactive WhatsApp Message
```javascript
const interactiveMessage = {
  to: '+1234567890',
  type: 'interactive',
  interactive: {
    type: 'button',
    body: {
      text: 'Would you like to confirm your appointment?'
    },
    action: {
      buttons: [
        {
          type: 'reply',
          reply: {
            id: 'confirm_yes',
            title: 'Yes, Confirm'
          }
        },
        {
          type: 'reply',
          reply: {
            id: 'confirm_no', 
            title: 'Reschedule'
          }
        }
      ]
    }
  }
};
```

### Voice & Phone Call Campaigns

#### Create Auto Dialer Campaign
```python
voice_campaign = {
    "name": "Appointment Reminder Campaign",
    "script": "Hello {first_name}, this is a reminder about your appointment on {appointment_date}. Press 1 to confirm or 2 to reschedule.",
    "contacts": [
        {
            "phone": "+1234567890",
            "first_name": "John",
            "appointment_date": "March 15th"
        }
    ],
    "schedule_time": "2024-03-14T09:00:00Z",
    "max_call_duration": 60,
    "retry_attempts": 3
}

response = requests.post(
    "https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/auto_dialer_campaigns",
    headers=headers,
    json=voice_campaign
)
print(f"Voice campaign created: {response.json()}")
```

#### Handle Call Callbacks
```javascript
// Webhook endpoint to handle call completion
app.post('/call-webhook', (req, res) => {
  const callEvent = req.body;

  console.log('Call completed:', {
    campaign_id: callEvent.campaign_id,
    contact_phone: callEvent.contact_phone,
    call_duration: callEvent.call_duration,
    call_status: callEvent.call_status,
    user_response: callEvent.user_response
  });

  // Process call results
  if (callEvent.user_response === '1') {
    // Appointment confirmed
    updateAppointmentStatus(callEvent.contact_phone, 'confirmed');
  } else if (callEvent.user_response === '2') {
    // Reschedule requested
    scheduleFollowUp(callEvent.contact_phone);
  }

  res.status(200).send('OK');
});
```

## Multi-Channel Campaign Orchestration

### Coordinated Multi-Channel Campaign
```python
# Example: Birthday campaign across all channels
def create_birthday_campaign():
    # 1. Start with SMS
    sms_campaign = create_sms_campaign({
        "message": "🎉 Happy Birthday {first_name}! Use code BIRTHDAY20 for 20% off!"
    })

    # 2. Follow up with WhatsApp rich message
    whatsapp_followup = create_whatsapp_campaign({
        "template": "birthday_celebration",
        "media_url": "https://example.com/birthday-gif.gif"
    })

    # 3. Personal call for VIP customers
    vip_call_campaign = create_voice_campaign({
        "script": "Happy Birthday {first_name}! We have a special surprise for you...",
        "contact_filter": "vip_customers"
    })

    return {
        "sms_campaign_id": sms_campaign.id,
        "whatsapp_campaign_id": whatsapp_followup.id, 
        "voice_campaign_id": vip_call_campaign.id
    }
```

## Contact Management Across Channels

### Unified Contact Creation
```bash
# Add a contact with multi-channel preferences
curl -X POST "https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/contacts" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "whatsapp_opt_in": true,
    "sms_opt_in": true,
    "voice_opt_in": true,
    "preferred_channel": "whatsapp",
    "labels": ["customer", "vip"],
    "custom_fields": {
      "birthday": "1990-05-15",
      "preferences": "electronics",
      "timezone": "America/New_York"
    }
  }'
```

## Channel-Specific Best Practices

### SMS & MMS Best Practices
- Keep messages concise (160 characters for SMS)
- Include clear call-to-action
- Always provide opt-out instructions
- Use MMS for visual content and branding
- Respect quiet hours and time zones

### WhatsApp Best Practices  
- Use rich media to enhance engagement
- Leverage interactive buttons and quick replies
- Follow WhatsApp Business Policy guidelines
- Use template messages for notifications
- Personalize messages with customer data

### Voice Campaign Best Practices
- Keep scripts concise and clear
- Provide clear interaction options
- Respect do-not-call preferences
- Schedule calls during appropriate hours
- Include callback options for missed calls

## Analytics and Reporting

### Multi-Channel Analytics
```javascript
// Get comprehensive campaign analytics
const analytics = await fetch(`https://seax.seasalt.ai/api/v1/workspace/{workspace_id}/campaigns/{campaign_id}/analytics`, {
  headers: { 'Authorization': 'Bearer YOUR_API_KEY' }
});

const stats = await analytics.json();
console.log('Campaign Performance:', {
  sms: {
    sent: stats.sms_sent,
    delivered: stats.sms_delivered,
    response_rate: stats.sms_response_rate
  },
  whatsapp: {
    sent: stats.whatsapp_sent,
    delivered: stats.whatsapp_delivered,
    read_rate: stats.whatsapp_read_rate
  },
  voice: {
    calls_made: stats.voice_calls_made,
    calls_answered: stats.voice_calls_answered,
    completion_rate: stats.voice_completion_rate
  }
});
```

## Webhook Configuration

### Multi-Channel Webhook Events
```javascript
// Handle webhooks for all channels
app.post('/seax-webhook', (req, res) => {
  const event = req.body;

  switch(event.channel) {
    case 'sms':
      handleSmsEvent(event);
      break;
    case 'whatsapp':
      handleWhatsAppEvent(event);
      break;
    case 'voice':
      handleVoiceEvent(event);
      break;
  }

  res.status(200).send('OK');
});

function handleSmsEvent(event) {
  if (event.type === 'message.received') {
    console.log('SMS received:', event.message);
    // Handle incoming SMS
  }
}

function handleWhatsAppEvent(event) {
  if (event.type === 'message.delivered') {
    console.log('WhatsApp message delivered:', event.message_id);
    // Update delivery status
  }
}

function handleVoiceEvent(event) {
  if (event.type === 'call.completed') {
    console.log('Call completed:', event.call_details);
    // Process call results
  }
}
```

## Error Handling

Common HTTP status codes remain the same across all channels:
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (insufficient permissions)
- `422` - Unprocessable Entity (validation errors)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

### Channel-Specific Error Handling
```python
def handle_seax_error(response):
    if response.status_code == 422:
        error_data = response.json()

        if 'whatsapp' in error_data.get('channel', ''):
            print("WhatsApp error:", error_data.get('message'))
            # Handle WhatsApp-specific errors (template issues, etc.)

        elif 'voice' in error_data.get('channel', ''):
            print("Voice error:", error_data.get('message'))
            # Handle voice-specific errors (invalid phone, etc.)

        else:
            print("SMS error:", error_data.get('message'))
            # Handle SMS-specific errors
```

## Migration Guide

### Upgrading from SMS-Only Implementation
If you're currently using SeaX for SMS-only campaigns, you can easily add multi-channel capabilities:

1. **Update API calls** to specify channel types
2. **Add channel preferences** to existing contacts
3. **Create channel-specific templates** for consistent messaging
4. **Configure webhooks** for multi-channel events
5. **Update analytics** to track cross-channel performance

### Example Migration
```python
# Before: SMS-only campaign
old_campaign = {
    "message": "Sale ending soon!",
    "contacts": ["+1234567890"]
}

# After: Multi-channel campaign
new_campaign = {
    "name": "End of Sale Multi-Channel Push",
    "channels": {
        "sms": {
            "message": "⏰ Sale ending in 2 hours! Use LAST20 for 20% off",
            "contacts": sms_contacts
        },
        "whatsapp": {
            "template": "sale_ending_soon",
            "contacts": whatsapp_contacts
        },
        "voice": {
            "script": "This is a final reminder about our sale ending today...",
            "contacts": vip_contacts
        }
    }
}
```

## Support and Resources

### Getting Help

- **API Documentation**:
  [https://seax.seasalt.ai/seax-api/redoc/](https://seax.seasalt.ai/seax-api/redoc/)
- **Support Email**: info@seasalt.ai
- **Knowledge Base**: [https://wiki.seasalt.ai](https://wiki.seasalt.ai)
- **Multi-Channel Best Practices**:
  [https://docs.seasalt.ai/multi-channel](https://docs.seasalt.ai/multi-channel)

### Channel-Specific Resources

- **SMS Compliance Guide**:
  [https://docs.seasalt.ai/sms-compliance](https://docs.seasalt.ai/sms-compliance)
- **WhatsApp Business Policy**:
  [https://docs.seasalt.ai/whatsapp-policy](https://docs.seasalt.ai/whatsapp-policy)
- **Voice Campaign Best Practices**:
  [https://docs.seasalt.ai/voice-campaigns](https://docs.seasalt.ai/voice-campaigns)

For detailed implementation guides and advanced multi-channel use cases, refer
to the complete API documentation or contact Seasalt.ai support.
