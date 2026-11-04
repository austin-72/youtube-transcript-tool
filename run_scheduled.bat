@echo off
rem Used by the daily scheduled task: same as run.bat, but no pause and output goes to a log file.
cd /d "%~dp0"
if not exist "output" mkdir "output"
echo. >> "output\scheduled_runs.log"
echo ===== %date% %time% ===== >> "output\scheduled_runs.log"
rem once a week, pick up the newest yt-dlp (YouTube changes often)
".venv\Scripts\python.exe" yt.py selfupdate --if-older-than 7 >> "output\scheduled_runs.log" 2>&1
".venv\Scripts\python.exe" yt.py run >> "output\scheduled_runs.log" 2>&1
