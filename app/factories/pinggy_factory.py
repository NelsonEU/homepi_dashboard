import os
from datetime import datetime
from app.models.pinggy_model import PinggyModel
from app.utils.systemd import run_systemctl_action

PINGGY_SYSTEMD_SERVICE = os.getenv("MC_PINGGY_SERVICE")


def build() -> PinggyModel:
    status = run_systemctl_action("is-active", PINGGY_SYSTEMD_SERVICE)

    active = status["ok"] and status["stdout"].strip() == "active"

    since = None
    if active:
        info = run_systemctl_action(
            "show --property=ActiveEnterTimestamp --value",
            PINGGY_SYSTEMD_SERVICE,
        )

        raw = info["stdout"].strip()
        if raw:
            since = datetime.strptime(
                raw,
                "%a %Y-%m-%d %H:%M:%S %Z",
            )

    return PinggyModel(
        active=active,
        since=since,
    )
