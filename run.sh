#!/usr/bin/env bash
set -euo pipefail

cd /home/arnaud/dashboard_api

# Start uvicorn using the venv python explicitly
exec /home/arnaud/dashboard_api/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
