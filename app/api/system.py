from fastapi import APIRouter
from app.utils.system import (
    get_cpu_temperature,
    get_cpu_usage,
    get_ram_usage,
    get_disk_usage
)

router = APIRouter(
    prefix="/api/system",
    tags=["system"],
)


@router.get("")
def system():
    temp_info = get_cpu_temperature()

    return {
        "cpu": {
            "temperature":  get_cpu_temperature(),
            "usage": get_cpu_usage()
        },
        "memory": {
            "ram": get_ram_usage(),
            "disk": get_disk_usage()
        }
    }
