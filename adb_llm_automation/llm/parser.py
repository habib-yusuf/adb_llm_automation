from __future__ import annotations
import re
from typing import List
from ..actions.actions import Action, Plan

# A pragmatic, deterministic parser that covers common phrasing.
# You can extend this with LLM fallbacks (see openai_client) if nothing matches.

TAP_RE = re.compile(r"tap\s+(?:at\s+)?(\d+)\s*[x, ]\s*(\d+)", re.I)
SWIPE_RE = re.compile(r"swipe\s+from\s+(\d+)\s*[x, ]\s*(\d+)\s+to\s+(\d+)\s*[x, ]\s*(\d+)(?:\s+in\s*(\d+)ms)?", re.I)
TEXT_RE = re.compile(r"type\s+(.+)$", re.I)
KEY_RE = re.compile(r"key(?:event)?\s+(\d+)", re.I)
LAUNCH_RE = re.compile(r"launch\s+([a-zA-Z0-9_.]+)(?:/(\S+))?", re.I)
SCREENSHOT_RE = re.compile(r"screenshot(?:\s+to\s+(\S+))?", re.I)
SHELL_RE = re.compile(r"shell\s+(.+)$", re.I)


def parse_lines(lines: List[str]) -> Plan:
    steps: List[Action] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = TAP_RE.search(line)
        if m:
            x, y = map(int, m.groups())
            steps.append(Action(type="tap", x=x, y=y))
            continue
        m = SWIPE_RE.search(line)
        if m:
            x1, y1, x2, y2, d = m.groups()
            steps.append(Action(type="swipe", x=int(x1), y=int(y1), x2=int(x2), y2=int(y2), duration_ms=int(d or 300)))
            continue
        m = TEXT_RE.search(line)
        if m:
            steps.append(Action(type="text", value=m.group(1)))
            continue
        m = KEY_RE.search(line)
        if m:
            steps.append(Action(type="keyevent", value=m.group(1)))
            continue
        m = LAUNCH_RE.search(line)
        if m:
            pkg, act = m.groups()
            steps.append(Action(type="launch_app", package=pkg, activity=act))
            continue
        m = SCREENSHOT_RE.search(line)
        if m:
            steps.append(Action(type="screenshot", path=m.group(1) or "screencap.png"))
            continue
        m = SHELL_RE.search(line)
        if m:
            steps.append(Action(type="shell", shell_cmd=m.group(1)))
            continue
        # If no rule matched, keep as shell (last resort)
        steps.append(Action(type="shell", shell_cmd=line))
    return Plan(steps=steps)