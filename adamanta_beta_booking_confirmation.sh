#! /bin/sh
curl -X 'POST' \
  'https://seax.seasalt.ai/seax-api/api/v1/workspace/e54fc9d3-7b05-4bc8-8e2c-7c964400cd4a/general_campaigns/wabp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: 3eeeffe30e45d4213411b7f19eb6244f691be05e061af75e60bae03508c79e50' \
  -d '{
  "sender_whatsapp_number": "+5215578686501",
  "type": "whatsapp",
  "highly_structured_message": {
    "template": "beta_booking_confirmation",
    "language_code": "es_MX",
    "destinations": [
      {"destination": "+14437438423", 
       "components": [
          {
            "type": "body",
            "parameters": [
              {
                "type": "text",
                "parameter_name": "climber_first",
                "text": "xuchen"
              },
              {
                "type": "text",
                "parameter_name": "gym_name",
                "text": "Adamanta Boulders"
              },
              {
                "type": "text",
                "parameter_name": "gym_url",
                "text": "https://g.co/kgs/Ko4ExbG"
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
                "text": "unique_qr_code_link"
              }
            ]
          }
        ]
      }
    ]
  }
}'
