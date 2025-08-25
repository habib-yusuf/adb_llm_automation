from __future__ import annotations
from typing import Optional, List
from .core.adb_connector import ADBConnector
from .actions.action_dispatcher import execute
from .llm.parser import parse_lines


def run(
    commands: List[str],
    device: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    plan = parse_lines(commands)
    plan.dry_run = dry_run
    adb = ADBConnector(device_id=device)
    execute(plan.steps, adb, dry_run=dry_run)