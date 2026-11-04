# PyInstaller recipe for the one-file Windows program:  pyinstaller YouTubeTranscriptTool.spec
# (build_exe.bat runs this; GitHub builds it for every release - see .github/workflows/build-exe.yml)
from PyInstaller.utils.hooks import collect_submodules, copy_metadata

hidden = (collect_submodules("yt_transcripts") + collect_submodules("youtube_transcript_api")
          + ["socks", "sockshandler", "tkinter", "tkinter.ttk", "tkinter.scrolledtext", "tkinter.filedialog",
             "tkinter.messagebox", "tkinter.simpledialog"])

a = Analysis(
    ["exe_main.py"],
    pathex=["."],
    datas=[("config.example.toml", ".")] + copy_metadata("yt-dlp") + copy_metadata("youtube-transcript-api")
          + copy_metadata("requests") + copy_metadata("yt-dlp-ejs"),
    hiddenimports=hidden,
    excludes=["pytest", "hypothesis", "IPython", "matplotlib", "numpy"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="YouTubeTranscriptTool",
    console=True,  # so it also works from cmd and PowerShell...
    hide_console="hide-early",  # ...but double-clicked, the console Windows opens for it is hidden at once
    upx=False,
    runtime_tmpdir=None,
)
