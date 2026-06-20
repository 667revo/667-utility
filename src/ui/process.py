import psutil
import platform

def get_system_info() -> dict:
    return {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_name": platform.processor(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_usage": psutil.cpu_percent(interval=0.5),  # %
        "ram_total": psutil.virtual_memory().total / (1024**3),   # GB
        "ram_used": psutil.virtual_memory().used / (1024**3),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_total": psutil.disk_usage('/').total / (1024**3),
        "disk_used": psutil.disk_usage('/').used / (1024**3),
        "disk_percent": psutil.disk_usage('/').percent,
    }