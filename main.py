import time
import os
from pathlib import Path
from monitor import is_game_running
from sync import sync_directory, has_differences
from logger import log_info, log_err

def main(saves_root, interval_seconds):
    log_info(f"Monitoring REPO game every {interval_seconds} seconds...")

    backup_root = Path(os.getenv("APPDATA")).parent / "LocalLow" / "REPO_game_saves"
    backup_root.mkdir(parents=True, exist_ok=True)

    first_check = True

    while True:
        if is_game_running("REPO.exe"):
            log_info("Game is running. Checking for differences...")

            try:
                needs_push = has_differences(saves_root, backup_root)
                needs_restore = has_differences(backup_root, saves_root)

                if needs_push:
                    log_info("Differences found: syncing saves -> backup")
                    sync_directory(saves_root, backup_root, mode='push')

                if needs_restore:
                    log_info("Differences found: restoring backup -> saves")
                    sync_directory(backup_root, saves_root, mode='restore')

                if not needs_push and not needs_restore:
                    log_info("No differences found. Nothing to sync.")

            except Exception as e:
                log_err(f"Sync error: {e}")

            first_check = False

        else:
            if first_check:
                log_info("Game is not running. Waiting...")
                first_check = False
            else:
                log_info("Game still not running. Exiting.")
                break

        time.sleep(interval_seconds)

if __name__ == "__main__":
    home = Path.home()
    saves_path = home / "AppData" / "LocalLow" / "semiwork" / "Repo" / "saves"
    main(saves_path, interval_seconds=40)