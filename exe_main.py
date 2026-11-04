"""Entry point of the one-file Windows program (YouTubeTranscriptTool.exe, built with PyInstaller).

Double-clicked (no arguments): opens the window (the console Windows opens for it is hidden by the
PyInstaller loader - hide_console in YouTubeTranscriptTool.spec).
With arguments it is the command line tool:  YouTubeTranscriptTool.exe run -k "ai agents"
"""

import sys


def main() -> int:
    from yt_transcripts.paths import APP_DIR, resource

    cfg = APP_DIR / "config.toml"
    if not cfg.exists():  # first start: a settings file to edit, next to the .exe
        try:
            cfg.write_text(resource("config.example.toml").read_text(encoding="utf-8"), encoding="utf-8")
        except OSError:
            pass
    if len(sys.argv) <= 1:
        from yt_transcripts.cli import main as cli_main

        return cli_main(["gui"])
    from yt_transcripts.cli import main as cli_main

    return cli_main(sys.argv[1:])


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    sys.exit(main())
