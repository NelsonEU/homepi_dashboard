from typing import Optional, Literal
from app.models.cpu_model import CpuModel

import psutil

def build() -> CpuModel:
    temperature        = __get_cpu_temperature()
    temperature_status = __compute_temperature_status(temperature)
    usage              = __get_cpu_usage()

    return CpuModel(
        temperature=temperature,
        temperatureStatus=temperature_status,
        usage=usage
    )
    
def __get_cpu_temperature() -> Optional[float]:
    temperature = None
    try:
        temps = psutil.sensors_temperatures()
        if "cpu_thermal" in temps and temps["cpu_thermal"]:
            entry = temps["cpu_thermal"][0]
            temperature = round(entry.current, 1)
    except Exception:
        pass

    if temperature is None:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                milli = int(f.read().strip())
                temperature = round(milli / 1000.0, 1)
        except (FileNotFoundError, PermissionError, OSError):
            pass

    return temperature

def __compute_temperature_status(temperature: Optional[float]) -> Literal["normal", "warning", "critical", "unknown"]:
    status = None
    if temperature is None:
        status = "unknown"
    elif temperature >= CpuModel.CRITICAL_TEMPERATURE:
        status = "critical"
    elif temperature >= CpuModel.HIGH_TEMPERATURE:
        status = "warning"
    else:
        status = "normal"

    return status
  
def __get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=0.2)
  