#!/bin/bash
# update_openapi_client.sh
# Usage: ./update_openapi_client.sh [DJANGO_URL] [CLIENT_OUTPUT_PATH]
# Example: ./update_openapi_client.sh http://localhost:8000 ./_client

set -e

DJANGO_URL=${1:-http://localhost:8000}
CLIENT_OUTPUT_PATH=${2:-./_client}
SCHEMA_PATH="/tmp/openapi.json"

# Download OpenAPI schema as JSON
echo "Downloading OpenAPI schema from $DJANGO_URL/api/schema/ ..."
curl -s -H "Accept: application/json" "$DJANGO_URL/api/schema/" > "$SCHEMA_PATH"

if ! head -1 "$SCHEMA_PATH" | grep -q '{'; then
  echo "Error: Downloaded schema is not in JSON format."
  exit 1
fi

echo "Generating Python client in $CLIENT_OUTPUT_PATH ..."
openapi-python-client generate --path "$SCHEMA_PATH" --meta none --output-path "$CLIENT_OUTPUT_PATH" --overwrite

if [ $? -eq 0 ]; then
  echo "✅ OpenAPI client updated successfully."
else
  echo "❌ Failed to update OpenAPI client."
  exit 1
fi 