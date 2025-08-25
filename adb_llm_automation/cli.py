from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional
import typer
from rich import print
from .runner import run
from .core.adb_connector import ADBConnector

app = typer.Typer(add_help_option=True)


@app.command()
def devices():
    """List"""