@echo off
rem Paste one or more YouTube links (or video IDs) and download their transcripts right away.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run setup.bat first.
    pause
    exit /b 1
)
:again
echo.
set "LINKS="
set /p "LINKS=Paste YouTube link(s), separated by spaces (Enter to quit): "
if not defined LINKS exit /b 0
set "LINKS=%LINKS:"=%"
if not defined LINKS goto again
rem quoted as one argument so links with special characters are safe; the tool splits them on spaces
".venv\Scripts\python.exe" yt.py transcripts "%LINKS%"
goto again
