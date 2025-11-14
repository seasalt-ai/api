#! /bin/sh
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/ffffffff-abcd-4000-0000-000000000000/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: f0656ab41743c3b28169aea4135d03e5052ba7356341e129d8636c20fd12f2e7' \
  -d '{
  "sender_whatsapp_number": "+17622424368",
  "type": "whatsapp",
  "highly_structured_message": {
    "template": "test_info_udpate_buttons",
    "language_code": "en_US",
    "destinations": [
    { "destination": "+14437438423" },
    { "destination": "+14252987474" }
    ],
     "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "name",
            "text": "Xuchen"
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "email",
            "text": "info@seasalt.ai"
          },
          {
            "type": "text",
            "parameter_name": "name",
            "text": "Xuchen Kang"
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
