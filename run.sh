#!/usr/bin/env bash
set -euo pipefail

# Load prod env vars
source /home/arnaud/dashboard-api/dashboard.env # Env file path

# Move to project root
cd "$DASHBOARD_API_ROOT_DIR"

# Start uvicorn using the venv python explicitly
exec "$DASHBOARD_API_ROOT_DIR/.venv/bin/python" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
