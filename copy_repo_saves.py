import time
import psutil
from pathlib import Path
import shutil
import os
from datetime import datetime, timedelta
import logging

LOG_FILE = "repo_copy.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def log_info(msg): logging.info(msg)
def log_warn(msg): logging.warning(msg)
def log_err(msg):  logging.error(msg)

def is_game_running(process_name):
    found = False
    for proc in psutil.process_iter(attrs=['name', 'pid']):
        try:
            name = proc.info['name']
            if process_name.lower() in name.lower():
                log_info(f"Game process found: {name} (PID: {proc.info['pid']})")
                found = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            log_warn(f"Failed to retrieve process info: {e}")
    if not found:
        log_info(f"Process '{process_name}' not found among active processes")
    return found

def get_latest_modified_directory(path):
    dirs = [d for d in Path(path).iterdir() if d.is_dir()] # list comprehension
    if not dirs:
        return None
    modified_dir = max(dirs, key=lambda d: d.stat().st_mtime)
    return modified_dir

def copy_and_sync_latest_save(path):
    modified_dir_path = Path(path)
    if not modified_dir_path.exists() or not modified_dir_path.is_dir():
        raise ValueError(f"Path does not exist or is not a directory: {modified_dir_path}")

    local_low_dir = Path(os.getenv("APPDATA")).parent / "LocalLow"
    destination_root = local_low_dir / "REPO_game_saves"
    destination_root.mkdir(parents=True, exist_ok=True)

    destination = destination_root / modified_dir_path.name
    destination.mkdir(parents=True, exist_ok=True)

    for item in modified_dir_path.rglob("*"):
        relative_path = item.relative_to(modified_dir_path)
        resulted_destination = destination / relative_path

        try:
            if item.is_dir():
                resulted_destination.mkdir(parents=True, exist_ok=True)
            else:
                # Copy if the file doesn't exist yet or is older
                # The file in the source is newer than the already copied file in the destination.
                if not resulted_destination.exists() or item.stat().st_mtime > resulted_destination.stat().st_mtime:
                    shutil.copy2(item, resulted_destination)
                    log_info(f"Updated file: {relative_path}")
                else:
                    log_info(f"Skipped (up-to-date): {relative_path}")
        except Exception as e:
            log_warn(f"Failed to process '{relative_path}': {e}")

    log_info(f"Synced '{modified_dir_path.name}' to '{destination_root}'")

def main(save_source_path, interval_seconds):
    log_info(f"Starting REPO game monitoring every {interval_seconds} seconds...")

    first_check = True # tracks the first cycle of checking the game's status

    while True:
        if is_game_running("REPO.exe"):
            log_info("Game is running, performing copy...")
            latest_modified_dir = get_latest_modified_directory(save_source_path)

            if latest_modified_dir:
                try:
                    copy_and_sync_latest_save(latest_modified_dir)
                except Exception as e:
                    log_err(f"Copy error: {e}")
            else:
                log_warn("No subdirectories found.")

            first_check = False

        else:
            if first_check:
                log_info("REPO game is not running. Waiting for next check...")
                first_check = False
            else:
                log_info("REPO game is still not running. Exiting script.")
                break

        time.sleep(interval_seconds)

if __name__ == "__main__":
    home_dir = Path.home()
    repo_saves_path = home_dir / "AppData" / "LocalLow" / "semiwork" / "Repo" / "saves"
    main(repo_saves_path, interval_seconds=40)
