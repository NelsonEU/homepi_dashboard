from typing import Optional, Literal, ClassVar
from pydantic import BaseModel

class CpuModel(BaseModel):
  HIGH_TEMPERATURE: ClassVar[float]     = 80.0
  CRITICAL_TEMPERATURE: ClassVar[float] = 90.0
  
  high_temperature: int = HIGH_TEMPERATURE
  critical_temperature: int = CRITICAL_TEMPERATURE
  temperature: Optional[float]
  temperatureStatus: Literal["normal", "warning", "critical"]
  usage: float