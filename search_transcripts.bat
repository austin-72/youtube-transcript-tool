@echo off
rem Search all downloaded transcripts for a word or phrase; prints links that jump to the moment.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run setup.bat first.
    pause
    exit /b 1
)
:again
echo.
set "PHRASE="
set /p "PHRASE=Search transcripts for (Enter to quit): "
if not defined PHRASE exit /b 0
rem drop any quotes the user typed - the phrase is quoted below anyway
set "PHRASE=%PHRASE:"=%"
if not defined PHRASE goto again
".venv\Scripts\python.exe" yt.py find "%PHRASE%"
goto again
