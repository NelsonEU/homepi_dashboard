import os
from app.utils.systemd import run_systemctl_action

PINGGY_SYSTEMD_SERVICE = os.getenv("MC_PINGGY_SERVICE")

def restart_pinggy():
    return run_systemctl_action("restart", PINGGY_SYSTEMD_SERVICE)
