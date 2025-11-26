# app/api/minecraft.py

from fastapi import APIRouter, Query
from app.models.minecraft_model import MinecraftModel
from app.factories import minecraft_factory
from app.utils.minecraft import get_minecraft_logs, start_minecraft, stop_minecraft, restart_minecraft

router = APIRouter(
    prefix="/api/minecraft",
    tags=["minecraft"],
)

    
@router.get("/activity", response_model=MinecraftModel)
def get_activity():
    return minecraft_factory.build()


@router.get("/logs")
def minecraft_logs(lines: int = Query(200, ge=10, le=1000)):
    return get_minecraft_logs(lines=lines)


@router.post("/start")
def minecraft_start():
    return start_minecraft()


@router.post("/stop")
def minecraft_stop():
    return stop_minecraft()


@router.post("/restart")
def minecraft_restart():
    return restart_minecraft()
