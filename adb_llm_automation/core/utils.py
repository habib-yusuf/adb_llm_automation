from __future__ import annotations
import shutil




def ensure_adb_available() -> None:
    if shutil.which("adb") is None:
        raise RuntimeError("adb not found on PATH. Install platform-tools and add to PATH.")