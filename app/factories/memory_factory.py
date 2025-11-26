from app.models.memory_model import MemoryModel, RamModel, DiskModel

import psutil

def build() -> MemoryModel:
    ram  = __get_ram_usage()
    disk = __get_disk_usage()

    return MemoryModel(ram=ram, disk=disk)

def __get_ram_usage() -> RamModel:
    mem = psutil.virtual_memory()
    return RamModel(
        total_bytes=mem.total,
        used_bytes=mem.used,
        percent=mem.percent,
        total_gb=__bytes_to_gb(mem.total),
        used_gb=__bytes_to_gb(mem.used)
    )

def __get_disk_usage() -> DiskModel:
    disk = psutil.disk_usage("/")
    return DiskModel(
        total_bytes=disk.total,
        used_bytes=disk.used,
        free_bytes=disk.free,
        percent=disk.percent,
        total_gb=__bytes_to_gb(disk.total),
        used_gb=__bytes_to_gb(disk.used),
        free_gb=__bytes_to_gb(disk.free),
    )
    
def __bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)

    