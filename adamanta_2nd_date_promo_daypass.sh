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
    "template": "2nd_date_promo_daypass",
    "language_code": "es_MX",
    "destinations": [
      {"destination": "+14437438423", 
       "components": [
          {
            "type": "body",
            "parameters": [
              {
                "type": "text",
                "text": "xuchen"
              }
            ]
          }
        ]
      }
    ]
  }
}'
