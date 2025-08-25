# adb_llm_automation/core/utils.py
import shutil
import subprocess

def is_adb_available() -> bool:
    """Check if adb is installed and available in PATH."""
    adb_path = shutil.which("adb")
    if adb_path is None:
        return False

    try:
        subprocess.run(
            ["adb", "version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except Exception:
        return False