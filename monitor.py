import psutil
from logger import log_info, log_err

def is_game_running(process_name):
    for proc in psutil.process_iter(attrs=['name', 'pid']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                log_info(f"Game process found: {proc.info['name']} (PID: {proc.info['pid']})")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    log_info(f"Process '{process_name}' not found.")
    return False