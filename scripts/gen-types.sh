#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Export the OpenAPI spec from the backend
cd "$ROOT_DIR/backend"
python3 export_openapi.py "$ROOT_DIR/frontend/openapi.json"

# Generate TypeScript types from the spec
cd "$ROOT_DIR/frontend"
npx openapi-typescript openapi.json -o src/api/types.ts

echo "TypeScript types generated at frontend/src/api/types.ts"
