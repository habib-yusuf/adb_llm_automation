import time
import os
from adb_connector import run_adb_command

def perform_tap(target):
    if target["type"] == "text":
        print(f"[INFO] Simulated tap on text: {target['value']}")
        return
    elif target["type"] == "coords":
        x, y = target["x"], target["y"]
        return run_adb_command(["shell", "input", "tap", str(x), str(y)])
    return "Invalid tap target"

def input_text(text):
    safe_text = text.replace(" ", "%s")
    print(f"[INFO] Inputting text: {text}")
    return run_adb_command(["shell", "input", "text", safe_text])

def take_screenshot(save_path="screenshot.png"):
    timestamp = int(time.time())
    device_path = f"/sdcard/screen_{timestamp}.png"
    local_path = os.path.abspath(save_path)

    print("[INFO] Taking screenshot...")
    run_adb_command(["shell", "screencap", "-p", device_path])
    run_adb_command(["pull", device_path, local_path])
    run_adb_command(["shell", "rm", device_path])
    print(f"[INFO] Screenshot saved to {local_path}")
    return local_path


def dispatch_action(action_json):
    action = action_json['action']
    target = action_json.get('target', {})

    if action == "tap":
        return perform_tap(target)
    elif action == "input_text":
        return input_text(target.get('value'))
    elif action == "screenshot":
        return take_screenshot()
    else:
        return f"Unsupported action: {action}"
