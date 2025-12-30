from typing import Dict, Any
import subprocess


def run_systemctl_action(
    action: str,
    service: str,
) -> Dict[str, Any]:
    cmd = ["sudo", "systemctl", action, service]

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "ok":         completed.returncode == 0,
            "stdout":     completed.stdout,
            "stderr":     completed.stderr,
            "returncode": completed.returncode,
        }
    except Exception as e:
        return {
            "ok":         False,
            "stdout":     "",
            "stderr":     str(e),
            "returncode": None,
        }
