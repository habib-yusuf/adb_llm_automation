from __future__ import annotations
from typing import Iterable
from .actions import Action
from ..core.adb_connector import ADBConnector


def execute(actions: Iterable[Action], adb: ADBConnector, dry_run: bool = False) -> None:
    for step in actions:
        if dry_run:
            print(f"[DRY] {step.model_dump()}")
            continue
        t = step.type
        if t == "tap":
            adb.tap(step.x, step.y)  # type: ignore[arg-type]
        elif t == "swipe":
            adb.swipe(step.x, step.y, step.x2, step.y2, step.duration_ms)  # type: ignore[arg-type]
        elif t == "text":
            adb.text(step.value or "")
        elif t == "keyevent":
            adb.keyevent(int(step.value))
        elif t == "launch_app":
            adb.launch_app(step.package or "", step.activity)
        elif t == "screenshot":
            adb.screenshot(step.path or "screencap.png")
        elif t == "shell":
            adb.shell(step.shell_cmd or "")
        else:
            raise ValueError(f"Unsupported action: {t}")