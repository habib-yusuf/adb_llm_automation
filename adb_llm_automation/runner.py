import typer
import time
from pathlib import Path
from adb_llm_automation.core.adb_connector import ADBConnector
from adb_llm_automation.core.utils import is_adb_available

app = typer.Typer()

@app.command("run-scenario")
def run_scenario(file: str):
    
    """Single execution file"""
    print("🚀 Single execution started")
    
    if not is_adb_available():
        print("❌ ADB is not available. Please install Android Platform Tools and add them to PATH.")
        raise typer.Exit(code=1)
    
    adb = ADBConnector()
    scenario_file = Path(file)
    
    if not scenario_file.exists():
        print(f"❌ Scenario file not found: {file}")
        raise typer.Exit(code=1)
    else:
        print(f"📂 Scenario file: {file}")
        
        instructions = scenario_file.read_text().strip()
        print(f"📄 Loaded scenario instructions:\n{instructions}\n")
        
        lower_instructions = instructions.lower()

    if "open" in lower_instructions and "close" in lower_instructions:
        print("⚡ Executing ADB commands...")
        adb.run_command("monkey -p com.swaglabsmobileapp -c android.intent.category.LAUNCHER 1")
        time.sleep(10)
        adb.run_command("am force-stop com.swaglabsmobileapp")
        print("✅ Scenario executed: Open and Close App")
    else:
        print("⚠️ No matching automation steps for this scenario.")

if __name__ == "__main__":
    app()