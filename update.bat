@echo off
rem YouTube changes often. If searches or transcripts start failing, run this to get the newest yt-dlp.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run setup.bat first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" yt.py selfupdate
".venv\Scripts\python.exe" -m pip install --upgrade "yt-dlp[curl-cffi]" --quiet >nul 2>nul
".venv\Scripts\python.exe" yt.py doctor
pause
