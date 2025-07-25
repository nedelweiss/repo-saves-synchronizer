import shutil
from pathlib import Path
from logger import log_info, log_warn

def has_differences(source_root, target_root):
    source_root = Path(source_root)
    target_root = Path(target_root)

    for subdir in source_root.iterdir():
        if not subdir.is_dir():
            continue

        target_subdir = target_root / subdir.name
        if not target_subdir.exists():
            return True

        for item in subdir.rglob("*"):
            relative_path = item.relative_to(subdir)
            destination = target_subdir / relative_path

            if not destination.exists():
                return True
            if item.is_file() and item.stat().st_mtime > destination.stat().st_mtime:
                return True

    return False

def sync_directory(source_root, target_root, *, mode):
    source_root = Path(source_root)
    target_root = Path(target_root)

    for subdir in source_root.iterdir():
        if not subdir.is_dir():
            continue

        target_subdir = target_root / subdir.name
        target_subdir.mkdir(parents=True, exist_ok=True)

        updated_files = 0
        skipped_files = 0

        for item in subdir.rglob("*"):
            relative_path = item.relative_to(subdir)
            destination = target_subdir / relative_path

            try:
                if item.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    if mode == 'push':
                        if not destination.exists() or item.stat().st_mtime > destination.stat().st_mtime:
                            shutil.copy2(item, destination)
                            log_info(f"UPDATED: {subdir.name}/{relative_path}")
                            updated_files += 1
                        else:
                            skipped_files += 1
                    elif mode == 'restore':
                        if not destination.exists():
                            shutil.copy2(item, destination)
                            log_info(f"RESTORED: {subdir.name}/{relative_path}")
                            updated_files += 1
            except Exception as e:
                log_warn(f"Failed to process '{subdir.name}/{relative_path}': {e}")

        if updated_files == 0 and skipped_files > 0:
            log_info(f"All files in '{subdir.name}' are UP-TO-DATE.")