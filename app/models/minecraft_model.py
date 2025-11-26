from pydantic import BaseModel
from typing import Optional, List, Literal
from app.models.memory_model import MemoryModel


class MinecraftPlayersModel(BaseModel):
    online: int
    max: int
    sample_names: List[str] = []


class MinecraftProcessModel(BaseModel):
    ok: bool
    state: str
    error: Optional[str] = None


class MinecraftModel(BaseModel):
    online: bool
    latency_ms: Optional[float] = None
    version: Optional[str] = None
    players: Optional[MinecraftPlayersModel] = None
    error: Optional[str] = None
    process: MinecraftProcessModel
    cpu_percent: float
    mood: Literal["offline", "chill", "normal", "busy"]
