import psutil

HIGH_TEMPERATURE_VALUE = 80.0
CRITICAL_TEMPERATURE_VALUE = 90.0

def _bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=0.2)


def get_ram_usage() -> dict:
    mem = psutil.virtual_memory()
    return {
        "total_bytes": mem.total,
        "used_bytes": mem.used,
        "percent": mem.percent,
        "total_gb": _bytes_to_gb(mem.total),
        "used_gb": _bytes_to_gb(mem.used),
    }


def get_disk_usage() -> dict:
    disk = psutil.disk_usage("/")
    return {
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free,
        "percent": disk.percent,
        "total_gb": _bytes_to_gb(disk.total),
        "used_gb": _bytes_to_gb(disk.used),
        "free_gb": _bytes_to_gb(disk.free),
    }


def get_cpu_temperature() -> dict:
    values = {"current": None, "high": HIGH_TEMPERATURE_VALUE, "critical": CRITICAL_TEMPERATURE_VALUE}

    try:
        temps = psutil.sensors_temperatures()
        if "cpu_thermal" in temps and temps["cpu_thermal"]:
            entry = temps["cpu_thermal"][0]
            values["current"] = round(entry.current, 1)
    except Exception:
        pass

    if values["current"] is None:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                milli = int(f.read().strip())
                values["current"] = round(milli / 1000.0, 1)
        except (FileNotFoundError, PermissionError, OSError):
            pass

    current = values["current"]

    if current is None:
        status = "unknown"
    elif current >= CRITICAL_TEMPERATURE_VALUE:
        status = "critical"
    elif current >= HIGH_TEMPERATURE_VALUE:
        status = "warning"
    else:
        status = "normal"

    return {
        "values": values,
        "status": status,
    }
