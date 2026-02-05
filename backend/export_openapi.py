"""Export FastAPI OpenAPI schema to a JSON file."""

import json
import sys

from app.main import app

schema = app.openapi()
out = sys.argv[1] if len(sys.argv) > 1 else "openapi.json"
with open(out, "w") as f:
    json.dump(schema, f, indent=2)
print(f"OpenAPI schema written to {out}")
