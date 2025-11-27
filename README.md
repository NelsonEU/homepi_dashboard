# HomePi Dashboard API

Backend service powering the HomePi Dashboard UI.
Built with **FastAPI**, protected with **Basic Auth**, and deployed as a
**systemd service** on a Raspberry Pi 5.

Frontend repository:
➡️ https://github.com/NelsonEU/homepi_dashboard_svelte

## Features

### System Endpoints

-   CPU usage, temperature, load
-   RAM + disk usage
-   Health/status checks

### Minecraft Endpoints

-   Start / Stop / Restart via systemd
-   Live server status (ping, latency, players, MOTD)
-   Log retrieval & tailing
-   Process monitoring

### Authentication

All endpoints are protected using **HTTP Basic Auth** with credentials.

## Deployment

Backend runs as a persistent **systemd service**.

### dashboard.service:

    [Unit]
    Description=HomePi Dashboard API
    After=network.target

    [Service]
    WorkingDirectory=/home/arnaud/dashboard_api
    ExecStart=/home/arnaud/dashboard_api/run.sh
    Restart=always
    User=arnaud

    [Install]
    WantedBy=multi-user.target

### run.sh

    #!/usr/bin/env bash
    set -euo pipefail

    cd /home/arnaud/dashboard_api
    exec /home/arnaud/dashboard_api/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000


## Frontend Integration

Static assets served from: `/public/`


## Development

    python3 -m venv .venv
    source .venv/bin/activate
    uvicorn app.main:app --reload

## 🔗 Related Repository

Frontend (Svelte):
➡️ https://github.com/NelsonEU/homepi_dashboard_svelte
