#!/bin/bash

ENV_FILE=./.env
API_KEY_PUBLIC_PREFIX=$(grep api_key_public_prefix $ENV_FILE | awk '{print $NF}')
API_KEY_SECRET=$(grep api_key_secret $ENV_FILE | awk '{print $NF}')

API_KEY="${API_KEY_PUBLIC_PREFIX}.${API_KEY_SECRET}"

ZONE=$( curl -s "https://api.hosting.ionos.com/dns/v1/zones" \
    -H "accept: application/json" \
    -H "X-API-Key: ${API_KEY}" \
    | jq -r '.[].id' )

curl -s "https://api.hosting.ionos.com/dns/v1/zones/${ZONE}?suffix=cabronita.com&recordType=A%2CCNAME" \
    -H "accept: application/json" \
    -H "X-API-Key: ${API_KEY}" \
    | jq -c '.records[]'

exit 0

### DOCS ###

Examples:
{
  "name": "bosch.cabronita.com",
  "rootName": "cabronita.com",
  "type": "A",
  "content": "192.168.1.41",
  "changeDate": "2025-02-10T19:38:46.152Z",
  "ttl": 3600,
  "disabled": false,
  "id": "bdc7db5a-0f3d-5c8a-d048-2d3dce83e6f6"
}

