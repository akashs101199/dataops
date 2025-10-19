#!/usr/bin/env bash
set -euo pipefail

# Init DB & admin (idempotent)
superset db upgrade
superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin || true
superset init

# Start the web server
exec superset run -h 0.0.0.0 -p 8088
