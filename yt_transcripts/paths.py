"""Where the tool's files live - next to yt.py normally, next to the .exe in the one-file Windows build."""

from __future__ import annotations

import sys
from pathlib import Path

FROZEN = bool(getattr(sys, "frozen", False))  # running as the PyInstaller .exe
# config.toml, output\ and tools\ live here (for the .exe: the folder the .exe is in)
APP_DIR = Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent.parent
# files shipped inside the program (config.example.toml); the .exe unpacks them to a temporary folder
BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
RELEASES_URL = "https://github.com/austin-72/youtube-transcript-tool/releases/latest"


def resource(name: str) -> Path:
    """A shipped file: the copy next to the program if there is one, else the bundled copy."""
    p = APP_DIR / name
    return p if p.exists() else BUNDLE_DIR / name
