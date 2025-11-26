from fastapi import APIRouter
from app.factories import cpu_factory
from app.factories import memory_factory
from app.models.memory_model import MemoryModel
from app.models.cpu_model import CpuModel

router = APIRouter(
    prefix="/api/system",
    tags=["system"],
)


@router.get("/cpu", response_model=CpuModel)
def get_cpu():
    return cpu_factory.build()


@router.get("/memory", response_model=MemoryModel)
def get_memory():
    return memory_factory.build()
