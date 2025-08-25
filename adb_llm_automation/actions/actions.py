from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional

ActionType = Literal[
    "tap", "swipe", "text", "keyevent", "launch_app", "screenshot", "shell"
]

class Action(BaseModel):
    type: ActionType
    x: Optional[int] = None
    y: Optional[int] = None
    x2: Optional[int] = None
    y2: Optional[int] = None
    duration_ms: int = 300
    value: Optional[str] = None
    package: Optional[str] = None
    activity: Optional[str] = None
    path: Optional[str] = Field(default=None, description="Local path for screenshot or file ops")
    shell_cmd: Optional[str] = None

class Plan(BaseModel):
    steps: list[Action]
    dry_run: bool = False