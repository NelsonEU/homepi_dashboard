# app/utils/minecraft.py

import os
import subprocess
from datetime import datetime
from typing import Dict, Any

from mcstatus import JavaServer

from app.utils.system import get_cpu_usage, get_ram_usage 

MC_HOST = "127.0.0.1"          
MC_PORT = 25565              
MC_ADDRESS = f"{MC_HOST}:{MC_PORT}"
MC_ROOT_DIR = "/home/arnaud/minecraft/creepers-du-nether"  
MC_SYSTEMD_SERVICE = "mc-cdn.service"  


def _get_java_server() -> JavaServer:
    """Return a JavaServer instance for our MC server."""
    return JavaServer.lookup(MC_ADDRESS)


def get_minecraft_status() -> Dict[str, Any]:
    """
    High-level status: online/offline, latency, basic info, players.
    """
    server = _get_java_server()

    try:
        status = server.status()
        online = True
        latency_ms = round(status.latency, 1)
        players_online = status.players.online
        players_max = status.players.max
        sample_names = []
        
        if status.players.sample:
            sample_names = [p.name for p in status.players.sample]

        version = getattr(status.version, "name", None)

        return {
            "online":     online,
            "latency_ms": latency_ms,
            "version":    version,
            "players": {
                "online":       players_online,
                "max":          players_max,
                "sample_names": sample_names,
            },
        }
    except Exception as e:
        # server offline, not reachable, or some network error
        return {
            "online":     False,
            "latency_ms": None,
            "version":    None,
            "players":    None,
            "error":      str(e),
        }


def get_minecraft_activity() -> Dict[str, Any]:
    """
    Approximate 'how is it feeling':
    - MC server online status & players
    - CPU usage (from system utils)
    - RAM usage (from system utils)
    - a simple qualitative label
    """
    status = get_minecraft_status()
    cpu_percent = get_cpu_usage()
    ram = get_ram_usage()

    if not status["online"]:
        mood = "offline"
    else:
        players = status["players"]["online"] if status["players"] else 0
        if cpu_percent < 30 and players <= 2:
            mood = "chill"
        elif cpu_percent < 70:
            mood = "normal"
        else:
            mood = "busy"

    return {
        "online":      status["online"],
        "latency_ms":  status["latency_ms"],
        "players":     status["players"],
        "cpu_percent": cpu_percent,
        "ram":         ram,
        "mood":        mood
    }



def get_minecraft_logs(lines: int = 200) -> Dict[str, Any]:
    """
    Return the last N lines of latest.log.
    """
    # TODO Arnaud


def _run_systemctl_action(action: str) -> Dict[str, Any]:
    """
    Run a systemctl action on the MC service.
    """
    
    cmd = ["sudo", "systemctl", action, MC_SYSTEMD_SERVICE]

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


def start_minecraft() -> Dict[str, Any]:
    return _run_systemctl_action("start")


def stop_minecraft() -> Dict[str, Any]:
    return _run_systemctl_action("stop")


def restart_minecraft() -> Dict[str, Any]:
    return _run_systemctl_action("restart")


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
