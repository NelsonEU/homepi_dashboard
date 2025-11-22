# app/api/minecraft.py

from fastapi import APIRouter, Query

from app.utils.minecraft import (
    get_minecraft_status,
    get_minecraft_activity,
    get_minecraft_logs,
    start_minecraft,
    stop_minecraft,
    restart_minecraft,
    get_minecraft_process_status,
)

router = APIRouter(
    prefix="/api/minecraft",
    tags=["minecraft"],
)


@router.get("/status")
def minecraft_status():
    """
    High-level status:
    - online/offline
    - latency
    - players (online / max / sample)
    - process state (systemd)
    """
    status = get_minecraft_status()
    process = get_minecraft_process_status()

    return {
        "network": status,   # online/latency/players
        "process": process,  # systemd state
    }


@router.get("/activity")
def minecraft_activity():
    """
    'How is it feeling' – CPU, RAM, players, latency, mood.
    """
    return get_minecraft_activity()


@router.get("/logs")
def minecraft_logs(lines: int = Query(200, ge=10, le=1000)):
    """
    Return the last N lines of the Minecraft log.
    """
    return get_minecraft_logs(lines=lines)


# ====== ACTIONS ======

@router.post("/start")
def minecraft_start():
    return start_minecraft()


@router.post("/stop")
def minecraft_stop():
    return stop_minecraft()


@router.post("/restart")
def minecraft_restart():
    return restart_minecraft()
