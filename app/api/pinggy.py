# app/api/pinggy.py

from fastapi import APIRouter, Query
from app.models.pinggy_model import PinggyModel
from app.factories import pinggy_factory
from app.utils.pinggy import restart_pinggy

router = APIRouter(
    prefix="/api/pinggy",
    tags=["pinggy"],
)

    
@router.get("/status", response_model=PinggyModel)
def get_activity():
    return pinggy_factory.build()


@router.post("/restart")
def pinggy_restart():
    return restart_pinggy()
