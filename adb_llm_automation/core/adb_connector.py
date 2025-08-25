from __future__ import annotations
import subprocess
from typing import List, Optional
from .utils import is_adb_available


class ADBConnector:
    def __init__(self, device_id: Optional[str] = None, adb_path: str = "adb"):
        self.device_id = device_id
        self.adb_path = adb_path
        is_adb_available()

    # --- internal helpers ---
    def _base_cmd(self) -> List[str]:
        cmd = [self.adb_path]
        if self.device_id:
            cmd += ["-s", self.device_id]
        return cmd

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        cmd = self._base_cmd() + list(args)
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=check)

    # --- device discovery ---
    @staticmethod
    def list_devices(adb_path: str = "adb") -> List[str]:
        res = subprocess.run([adb_path, "devices"], stdout=subprocess.PIPE, text=True, check=True)
        lines = [ln.strip() for ln in res.stdout.splitlines()[1:] if ln.strip()]
        return [ln.split()[0] for ln in lines if "device" in ln]

    # --- common actions ---
    def shell(self, cmd: str) -> str:
        return self._run("shell", cmd).stdout

    def tap(self, x: int, y: int) -> None:
        self.shell(f"input tap {x} {y}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")

    def text(self, value: str) -> None:
        safe = value.replace(" ", "%s")
        self.shell(f"input text {safe}")

    def keyevent(self, keycode: int) -> None:
        self.shell(f"input keyevent {keycode}")

    def launch_app(self, package: str, activity: Optional[str] = None) -> None:
        if activity:
            self.shell(f"am start -n {package}/{activity}")
        else:
            self.shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")

    def screenshot(self, dest_path: str) -> None:
        # Uses /sdcard/screencap.png as a temp location
        self.shell("screencap -p /sdcard/___tmp_screencap.png")
        self._run("pull", "/sdcard/___tmp_screencap.png", dest_path)
        self.shell("rm /sdcard/___tmp_screencap.png")

    def dump_ui(self) -> str:
        return self.shell("uiautomator dump /sdcard/___tmp_ui.xml && cat /sdcard/___tmp_ui.xml")

    def battery(self) -> str:
        return self.shell("dumpsys battery")
    
    def run_command(self, command: str):
        full_cmd = ["adb", "shell"] + command.split()
        print(f"🔧 Running command: {' '.join(full_cmd)}")  # Debug print
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        
        if result.stdout.strip():
            print("📤 STDOUT:", result.stdout.strip())
        if result.stderr.strip():
            print("⚠️ STDERR:", result.stderr.strip())
        
        return result