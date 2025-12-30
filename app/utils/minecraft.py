# app/utils/minecraft.py

import os
import subprocess
from functools import lru_cache
from typing import Dict, Any
from mcstatus import JavaServer
from app.utils.systemd import run_systemctl_action

MC_SYSTEMD_SERVICE = os.getenv("MC_SERVER_SERVICE")
MC_ROOT_DIR = os.getenv('MC_SERVER_ROOT_DIR')
MC_HOST = os.getenv("MC_SERVER_HOST")
MC_PORT = os.getenv("MC_SERVER_PORT")
MC_ADDRESS = f"{MC_HOST}:{MC_PORT}"


@lru_cache(maxsize=1)
def get_server() -> JavaServer:
    """Low-level: return a cached JavaServer instance."""
    return JavaServer.lookup(MC_ADDRESS)


def get_minecraft_process_status() -> Dict[str, Any]:
    """
    Process-level status from systemd: active/inactive/failed/etc.
    """
    cmd = ["systemctl", "is-active", MC_SYSTEMD_SERVICE]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        state = completed.stdout.strip()
        return {
            "ok":      completed.returncode == 0,
            "state":   state
        }
    except Exception as e:
        return {"ok": False, "state": "unknown", "error": str(e)}
    

def get_minecraft_logs(lines: int = 200) -> Dict[str, Any]:
    """
    Return the last N lines of latest.log.
    """
    log_file = os.path.join(MC_ROOT_DIR, "logs", "latest.log")

    try:
        with open(log_file, "r", errors="replace") as f:
            all_lines = f.readlines()

        last_lines = all_lines[-lines:]
        text = "".join(last_lines)

        return {
            "ok": True,
            "lines": text,
            "count": len(last_lines),
            "path": log_file,
        }
    except FileNotFoundError:
        return {
            "ok": False,
            "error": f"log file not found at {log_file}",
            "lines": "",
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "lines": "",
        }


def start_minecraft() -> Dict[str, Any]:
    return run_systemctl_action("start", MC_SYSTEMD_SERVICE)


def stop_minecraft() -> Dict[str, Any]:
    return run_systemctl_action("stop", MC_SYSTEMD_SERVICE)


def restart_minecraft() -> Dict[str, Any]:
    return run_systemctl_action("restart", MC_SYSTEMD_SERVICE)
