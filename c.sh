#! /bin/sh
curl -X 'POST' \
  'https://seax-dev.seasalt.ai/seax-api/api/v1/workspace/28e365fd-ccf3-4bc1-935b-a5340287d76f/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: 7bc12bb47af2467282148a83afef6cadf21185bfcf0aedbdb84e304c8adb8e23' \
  -d '{
  "sender_whatsapp_number": "+13867033591",
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
