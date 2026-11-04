@echo off
rem Search YouTube, save the video list and download transcripts, using config.toml.
rem Extra options can be added, e.g.:  run.bat --min-views 50000 --within week
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run setup.bat first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" yt.py run --open %*
echo.
pause
