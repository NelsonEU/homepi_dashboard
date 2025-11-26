from pydantic import BaseModel

class RamModel(BaseModel):
    total_bytes: int
    used_bytes: int
    percent: float

    total_gb: float
    used_gb: float
    
class DiskModel(BaseModel):
    total_bytes: int
    used_bytes: int
    free_bytes: int
    percent: float

    total_gb: float
    used_gb: float
    free_gb: float

class MemoryModel(BaseModel):
    ram: RamModel
    disk: DiskModel
