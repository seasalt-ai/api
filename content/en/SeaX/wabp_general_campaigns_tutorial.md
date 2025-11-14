---
title: WhatsApp Business Platform General Campaigns API Tutorial
linkTitle: WABP General Campaigns Tutorial
description:
  Tutorial for using the /api/v1/workspace/{workspace_id}/general_campaigns/wabp
  endpoint to send WhatsApp template messages.
categories: [API, WhatsApp Campaign, Messaging, Templates]
tags:
  [
    whatsapp,
    business platform,
    general campaigns,
    templates,
    highly structured messages,
  ]
type: docs
weight: 5
---

# WhatsApp Business Platform General Campaigns API Tutorial

## Overview

The `/api/v1/workspace/{workspace_id}/general_campaigns/wabp` endpoint allows
you to send WhatsApp Business Platform (WABP) template messages to multiple
destinations in a single API call. This is ideal for sending highly structured
messages using approved WhatsApp templates with personalized parameters.

### Key Features

- **Template-based Messaging**: Send messages using pre-approved WhatsApp
  templates
- **Multi-destination Support**: Send to multiple recipients in one request
- **Parameter Substitution**: Personalize messages with dynamic parameters
- **Language Support**: Use templates in different languages

## Prerequisites

Before using this endpoint, ensure you have:

1. A verified WhatsApp Business account
2. Approved WhatsApp message templates
3. A valid API Key for authorization
4. Your workspace ID

## Endpoint Details

**Endpoint**:
`POST https://seax.seasalt.ai/seax-api/api/v1/workspace/{workspace_id}/general_campaigns/wabp`

## Authorization

All requests must include your API Key in the `X-API-Key` header.

```bash
-H 'X-API-Key: {YOUR_API_KEY}'
```

#### Setting Up Your API Key

1. Navigate to **Account → API Key** tab in your dashboard.
2. Generate or refresh your API Key if necessary.
3. Copy the API Key and store it securely.

> **Note**: Keep your API key confidential to ensure the security of your
> service.

## Request Body Structure

The request body consists of the following fields:

| Field                                                  | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                            | Required    |
| ------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `sender_whatsapp_number`                               | `string` | Your WhatsApp Business phone number (E.164 format)                                                                                                                                                                                                                                                                                                                                                                     | ✅          |
| `type`                                                 | `string` | Message type (must be `"whatsapp"`)                                                                                                                                                                                                                                                                                                                                                                                    | ✅          |
| `highly_structured_message`                            | `object` | Contains template details and destinations                                                                                                                                                                                                                                                                                                                                                                             | ✅          |
| `highly_structured_message.template`                   | `string` | Name of the approved WhatsApp template                                                                                                                                                                                                                                                                                                                                                                                 | ✅          |
| `highly_structured_message.language_code`              | `string` | Language code of the template (e.g., `en_US`, `es`)                                                                                                                                                                                                                                                                                                                                                                    | ✅          |
| `highly_structured_message.destinations`               | `array`  | List of recipient destinations                                                                                                                                                                                                                                                                                                                                                                                         | ✅          |
| `highly_structured_message.destinations[].destination` | `string` | Recipient phone number (E.164 format)                                                                                                                                                                                                                                                                                                                                                                                  | ✅          |
| `highly_structured_message.components`                 | `array`  | **Campaign-level components** - Template components (header, body, buttons) with parameters. Applied to all destinations unless overridden. Uses the same structure as [Meta's Components API](https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/components). See [Postman reference](https://www.postman.com/meta/whatsapp-business-platform/folder/dybfz7u/components-object). | Conditional |
| `highly_structured_message.destinations[].components`  | `array`  | **Destination-specific components** - Override campaign-level components for individual recipients to send personalized content. Same structure as campaign-level components.                                                                                                                                                                                                                                          | Conditional |

## Components Structure

The `components` field provides a flexible way to send template messages with
support for header, body, and button parameters. This field uses the same
structure as
[Meta's WhatsApp Components API](https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/components)
([Postman reference](https://www.postman.com/meta/whatsapp-business-platform/folder/dybfz7u/components-object)).

### Two Ways to Use Components

**1. Campaign-Level Components (Global)** - Apply the same parameters to all
recipients:

```json
{
  "template": "welcome_message",
  "language_code": "en_US",
  "destinations": [
    { "destination": "+11234567890" },
    { "destination": "+10987654321" }
  ],
  "components": [
    {
      "type": "body",
      "parameters": [
        { "type": "text", "parameter_name": "company", "text": "Seasalt.ai" }
      ]
    }
  ]
}
```

**2. Destination-Specific Components (Personalized)** - Customize parameters for
each recipient:

```json
{
  "template": "welcome_message",
  "language_code": "en_US",
  "destinations": [
    {
      "destination": "+11234567890",
      "components": [
        {
          "type": "body",
          "parameters": [
            { "type": "text", "parameter_name": "name", "text": "Alice" }
          ]
        }
      ]
    },
    {
      "destination": "+10987654321",
      "components": [
        {
          "type": "body",
          "parameters": [
            { "type": "text", "parameter_name": "name", "text": "Bob" }
          ]
        }
      ]
    }
  ]
}
```

**Note**: If both campaign-level and destination-specific components are
provided, the destination-specific components take priority for that recipient.

Supported features:

- **Header parameters**: Text, images, videos, documents
- **Body parameters**: Named or positional text parameters
- **Button parameters**: Dynamic URLs and coupon codes
- **Footer**: Static text (defined in template or via API)

### Component Types

1. **Header Component** (`type: "header"`)

   - Text headers with no parameter syntax, named parameters, or positional
     parameters
   - Media headers (image, video, document)

2. **Body Component** (`type: "body"`)

   - Named parameters (e.g., `{{name}}`, `{{email}}`)
   - Positional parameters (e.g., `{{1}}`, `{{2}}`)

3. **Button Component** (`type: "button"`)

   - URL buttons with dynamic parameters in the url
   - Copy code buttons with dynamic coupon codes
   - Phone number buttons (static)
   - Quick reply buttons (static)

4. **Footer Component** (`type: "footer"`)

   - Static text footer
   - Defined in the template or can be passed via API

**Important**:

- Parameter names must be lowercase with underscores only (e.g., `product_name`,
  `user_email`)
- Button text and labels are defined in the template and cannot be changed via
  API
- Only URL parameters and coupon codes can be dynamically set

## Examples

### Example 1: Template with Header, Body, and Copy Code Button

This example sends the `test_coupon_code` template with a dynamic header, body
parameters, and a copy code button.

**Template**:

```
Header: Special offer on {{product}}!
Body: Hi {{name}}, get {{discount}}% off on {{product}}. Use the code below!
Button: [Copy Code] (copy_code button)
```

**cURL Command**:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/{workspace_id}/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: {YOUR_API_KEY}' \
  -d '{
  "sender_whatsapp_number": "+1123456789",
  "type": "whatsapp",
  "highly_structured_message": {
    "template": "test_coupon_code",
    "language_code": "en_US",
    "destinations": [
      {
        "destination": "+1987654321"
      }
    ],
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "product",
            "text": "Macbook Pro"
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "product",
            "text": "Macbook Pro"
          },
          {
            "type": "text",
            "parameter_name": "name",
            "text": "John Doe"
          },
          {
            "type": "text",
            "parameter_name": "discount",
            "text": "10"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "copy_code",
        "index": 0,
        "parameters": [
          {
            "type": "coupon_code",
            "coupon_code": "10PCNTOFF"
          }
        ]
      }
    ]
  }
}'
```

**Request Body Breakdown**:

- **Sender**: `+1123456789` (your WhatsApp Business number)
- **Template**: `test_coupon_code` in English (US)
- **Recipient**: `+1987654321`
- **Components**:
  - **Header**: Product name "Macbook Pro"
  - **Body**: Product, name, and discount percentage
  - **Button**: Copy code button with coupon "10PCNTOFF"

**Message Received**:

```
Special offer on Macbook Pro!
Hi Kelly Kang, get 10% off on Macbook Pro. Use the code below!
[Copy Code: 10PCNTOFF]
```

---

### Example 2: Template with Multiple URL Buttons

This example sends the `test_info_update_buttons` template with a header, body
parameters, and two URL buttons with dynamic parameters.

**Template**:

```
Header: Hi {{name}}!
Body: Your info: {{email}}, {{name}}, {{info}}
Button 1: [Learn More] → https://seasalt.ai/products/{{1}}
Button 2: [Get Started] → https://seasalt.ai/products/{{1}}
```

**cURL Command**:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/{workspace_id}/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: {YOUR_API_KEY}' \
  -d '{
  "sender_whatsapp_number": "+1123456789",
  "type": "whatsapp",
  "highly_structured_message": {
    "template": "test_info_update_buttons",
    "language_code": "en_US",
    "destinations": [
      {
        "destination": "+1987654321"
      }
    ],
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "name",
            "text": "John Doe"
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "email",
            "text": "info@email.com"
          },
          {
            "type": "text",
            "parameter_name": "name",
            "text": "John Doe"
          },
          {
            "type": "text",
            "parameter_name": "info",
            "text": "Seattle 98133"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": 0,
        "parameters": [
          {
            "type": "text",
            "text": "seavoice"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": 1,
        "parameters": [
          {
            "type": "text",
            "text": "seachat"
          }
        ]
      }
    ]
  }
}'
```

**Request Body Breakdown**:

- **Sender**: `+1123456789`
- **Template**: `test_info_update_buttons` in English (US)
- **Recipient**: `+1987654321`
- **Components**:
  - **Header**: Name "John Doe"
  - **Body**: Email, name, and info
  - **Button 1**: URL with parameter "seavoice" →
    `https://seasalt.ai/products/seavoice`
  - **Button 2**: URL with parameter "seachat" →
    `https://seasalt.ai/products/seachat`

**Message Received**:

```
Hi John Doe!
Your info: info@email.com, John Doe, Seattle 98133
[Learn More] → https://seasalt.ai/products/seavoice
[Get Started] → https://seasalt.ai/products/seachat
```

**Key Feature**: URL buttons can have dynamic parameters that are substituted at
send time, allowing for personalized links per recipient.

---

### Example 3: Template with Positional Parameters (No Named Parameters)

This example sends the `test_info_update_positional` template using positional
parameters ({{1}}, {{2}}, {{3}}) instead of named parameters.

**Template**:

```
Hi {{1}}, your information has been successfully updated to {{2}}. Contact {{3}} for any inquiries.
```

**cURL Command**:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/{workspace_id}/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: {YOUR_API_KEY}' \
  -d '{
  "sender_whatsapp_number": "+1123456789",
  "type": "whatsapp",
  "highly_structured_message": {
    "template": "test_info_update_positional",
    "language_code": "en_US",
    "destinations": [
      {
        "destination": "+1987654321"
      }
    ],
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
            "text": "Seattle 98133"
          },
          {
            "type": "text",
            "text": "info@email.com"
          }
        ]
      }
    ]
  }
}'
```

**Request Body Breakdown**:

- **Sender**: `+1123456789`
- **Template**: `test_info_update_positional` in English (US)
- **Recipient**: `+1987654321`
- **Components**:
  - **Body**: Three positional parameters (no `parameter_name` field)
    - Position {{1}}: "John Doe"
    - Position {{2}}: "Seattle 98133"
    - Position {{3}}: "info@email.com"

**Message Received**:

```
Hi John Doe, your information has been successfully updated to Seattle 98133. Contact info@email.com for any inquiries.
```

**Key Difference**: For positional parameters, you omit the `parameter_name`
field. The order of parameters in the array corresponds to the position numbers
in the template ({{1}}, {{2}}, {{3}}).

---

### Example 4: Template without Parameters

This example sends a simple template called `test_hola` in Spanish that doesn't
require any parameters or components.

**cURL Command**:

```bash
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/{workspace_id}/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: {YOUR_API_KEY}' \
  -d '{
  "sender_whatsapp_number": "+1123456789",
  "type": "whatsapp",
  "highly_structured_message": {
    "template": "test_hola",
    "language_code": "es",
    "destinations": [
      {
        "destination": "+15552341345"
      }
    ]
  }
}'
```

**Request Body Breakdown**:

- **Sender**: `+13867033591`
- **Template**: `test_hola` in Spanish
- **Recipient**: `+15552341345`
- **Components**: None (template is static with no dynamic content)

**Use Case**: This is ideal for simple notification templates that don't need
personalization, such as "Hola!" or "Thank you for your order!"

## Response Format

**Success Response (200 OK)**:

```json
{
  "id": "campaign_12345678-abcd-efgh-ijkl-123456789012",
  "status": "sending",
  "created_time": "2025-10-24T21:00:00.000Z",
  "total_destinations": 1,
  "job_id": "job_12345678-abcd-efgh-ijkl-123456789012"
}
```

**Response Fields**:

- `id`: Unique identifier for the campaign
- `status`: Current status (e.g., `sending`, `sent`, `finished`)
- `created_time`: Campaign creation timestamp
- `total_destinations`: Number of recipients
- `job_id`: Job ID for tracking campaign progress

## Error Handling

### Common Errors

#### 401 Unauthorized

```json
{
  "error": "Unauthorized",
  "message": "Invalid API Key"
}
```

**Solution**: Verify your API Key is correct and active.

#### 400 Bad Request - Invalid Template

```json
{
  "error": "Bad Request",
  "message": "Template not found or not approved",
  "details": {
    "template": "test_info_update",
    "language_code": "en_US"
  }
}
```

**Solution**: Ensure the template name and language code match an approved
template in your WhatsApp Business account.

#### 400 Bad Request - Invalid Phone Number

```json
{
  "error": "Bad Request",
  "message": "Invalid phone number format",
  "details": {
    "field": "sender_whatsapp_number",
    "value": "+1234567890"
  }
}
```

**Solution**: Use E.164 format for phone numbers (e.g., `+15552341345`).

#### 400 Bad Request - Missing Parameters

```json
{
  "error": "Bad Request",
  "message": "Required template parameter missing",
  "details": {
    "missing_parameter": "name",
    "template": "test_info_update"
  }
}
```

**Solution**: Ensure all required template parameters are included in the
request.

#### 422 Unprocessable Entity

```json
{
  "error": "Validation Error",
  "message": "Invalid workspace_id format"
}
```

**Solution**: Check that your workspace ID is valid UUID format.

## Components Best Practices

### Parameter Naming Rules

When using the `parameter_name` field for templates with named placeholders:

- ✅ **Use lowercase letters and underscores only**: `product_name`,
  `user_email`, `discount_code`
- ❌ **Do not use**: Uppercase letters, hyphens, spaces, or camelCase
- Examples:
  - ✅ `product_name`
  - ✅ `user_email`
  - ✅ `first_name`
  - ❌ `Product_Name` (uppercase)
  - ❌ `product-name` (hyphens)
  - ❌ `product name` (spaces)
  - ❌ `productName` (camelCase)

### Template Types

**Templates with Named Placeholders** (e.g., `{{name}}`, `{{email}}`):

```json
{
  "type": "body",
  "parameters": [
    { "type": "text", "parameter_name": "name", "text": "Kelly Kang" },
    { "type": "text", "parameter_name": "email", "text": "info@seasalt.ai" }
  ]
}
```

**Templates with Positional Placeholders** (e.g., `{{1}}`, `{{2}}`, `{{3}}`):

```json
{
  "type": "body",
  "parameters": [
    { "type": "text", "text": "Kelly Kang" },
    { "type": "text", "text": "Seattle 98133" },
    { "type": "text", "text": "info@seasalt.ai" }
  ]
}
```

**Important**: Match your request to your template type:

- If your template uses `{{name}}`, `{{email}}` → include `parameter_name` field
- If your template uses `{{1}}`, `{{2}}` → omit `parameter_name` field

### Button Types and Parameters

1. **URL Buttons**: Can have dynamic URL parameters

   ```json
   {
     "type": "button",
     "sub_type": "url",
     "index": 0,
     "parameters": [{ "type": "text", "text": "user123" }]
   }
   ```

2. **Copy Code Buttons**: Require coupon code parameter

   ```json
   {
     "type": "button",
     "sub_type": "copy_code",
     "index": 0,
     "parameters": [{ "type": "coupon_code", "coupon_code": "SAVE20" }]
   }
   ```

3. **Phone/Quick Reply Buttons**: No parameters needed
   ```json
   {
     "type": "button",
     "sub_type": "phone_number",
     "index": 0,
     "parameters": []
   }
   ```

**Note**: Button text and labels are defined in the template and **cannot be
changed** via API. Only URL parameters and coupon codes can be customized.

## Best Practices

### 1. Template Management

- **Use Approved Templates**: Only use WhatsApp-approved templates to avoid
  failures
- **Match Template Structure**: Ensure your components match the template's
  structure (header, body, buttons)
- **Parameter Naming**: Use lowercase + underscores for `parameter_name` (e.g.,
  `user_name`, not `userName`)
- **Choose Parameter Format**: Use named parameters for clarity or positional
  parameters for simplicity
- **Provide All Required Components**: Include all dynamic parts (header, body,
  buttons) that your template requires
- **Test Templates**: Test with a single destination before sending to multiple
  recipients

### 2. Phone Number Formatting

- **E.164 Format**: Always use international format with country code (e.g.,
  `+19876543210`)
- **Validation**: Validate phone numbers before sending to reduce errors
- **WhatsApp Registration**: Ensure recipients are registered on WhatsApp

### 3. Rate Limiting

- **Respect Limits**: Be aware of WhatsApp's messaging rate limits
- **Batch Wisely**: Don't send too many destinations in a single request
- **Monitor Responses**: Check campaign status and adjust send rates accordingly

### 4. Personalization

- **Dynamic Content**: Use parameters to personalize messages for each recipient
- **Data Validation**: Validate parameter values before substitution
- **Character Limits**: Be mindful of WhatsApp's character limits for template
  parameters

### 5. Error Handling

- **Retry Logic**: Implement retry logic for transient errors
- **Error Logging**: Log errors for debugging and monitoring
- **Fallback Strategy**: Have a fallback plan if template sending fails

## Language Codes

Common language codes for WhatsApp templates:

| Language              | Code    |
| --------------------- | ------- |
| English (US)          | `en_US` |
| Spanish               | `es`    |
| Spanish (Mexico)      | `es_MX` |
| Portuguese (Brazil)   | `pt_BR` |
| French                | `fr`    |
| German                | `de`    |
| Italian               | `it`    |
| Chinese (Simplified)  | `zh_CN` |
| Chinese (Traditional) | `zh_TW` |
| Japanese              | `ja`    |
| Korean                | `ko`    |

Here is a complete list of supported language:
[link](https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/supported-languages/)
