# app/factories/minecraft_factory.py

from typing import Optional, Literal
from app.models.minecraft_model import MinecraftModel, MinecraftPlayersModel, MinecraftProcessModel
from app.factories import cpu_factory
from app.utils.minecraft import get_server, get_minecraft_process_status


def build() -> MinecraftModel:
    server = get_server()

    online: bool
    latency_ms: Optional[float]
    version: Optional[str]
    players_model: Optional[MinecraftPlayersModel]
    error: Optional[str]

    try:
        status        = server.status()
        online        = True
        latency_ms    = round(status.latency, 1)
        players_model = __build_minecraft_players_model(status)
        version       = getattr(status.version, "name", None)
        error         = None
    except Exception as e:
        online        = False
        latency_ms    = None
        version       = None
        players_model = None
        error         = str(e)

    process_model = __build_minecraft_process_model()
    cpu           = cpu_factory.build()
    mood          = __compute_mood(online=online, cpu_percent=cpu.usage, players_online=players_model.online if players_model else 0)

    return MinecraftModel(
        online=online,
        latency_ms=latency_ms,
        version=version,
        players=players_model,
        error=error,
        process=process_model,
        cpu_percent=cpu.usage,
        mood=mood,
    )


def __build_minecraft_players_model(status) -> Optional[MinecraftPlayersModel]:
    if not getattr(status, "players", None):
        return None

    players = status.players
    sample_names = []
    if players.sample:
        sample_names = [p.name for p in players.sample]

    return MinecraftPlayersModel(
        online=players.online,
        max=players.max,
        sample_names=sample_names,
    )


def __build_minecraft_process_model() -> MinecraftProcessModel:
    process_raw = get_minecraft_process_status()
    return MinecraftProcessModel(
        ok=process_raw["ok"],
        state=process_raw["state"],
        error=process_raw.get("error"),
    )


def __compute_mood(online: bool, cpu_percent: float, players_online: int) -> Literal["offline", "chill", "normal", "busy"]:
    if not online:
        return "offline"
    if cpu_percent < 30 and players_online <= 2:
        return "chill"
    elif cpu_percent < 70:
        return "normal"
    else:
        return "busy"
