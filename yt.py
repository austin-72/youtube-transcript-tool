#!/usr/bin/env python3
"""Entry point: python yt.py [run|search|transcripts|find|status|doctor|gui|init] ..."""

import sys
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit(
        f"This tool needs Python 3.11 or newer (you have {sys.version.split()[0]}).\n"
        "Install a newer Python from https://www.python.org/downloads/ and run setup.bat again."
    )

sys.path.insert(0, str(Path(__file__).resolve().parent))

from yt_transcripts.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
