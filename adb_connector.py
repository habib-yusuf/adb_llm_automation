import subprocess

def run_adb_command(command):
    result = subprocess.run(["adb"] + command, capture_output=True, text=True)
    return result.stdout.strip()

def handle_tap(target):
    if target["type"] == "coords":
        x, y = target["x"], target["y"]
        return run_adb_command(["shell", "input", "tap", str(x), str(y)])
    elif target["type"] == "text":
        # Use UIAutomator or OCR to find text position (advanced)
        return f"Text-based taps need element detection"
    return "Invalid target for tap"

def input_text(text):
    return run_adb_command(["shell", "input", "text", text.replace(" ", "%s")])
