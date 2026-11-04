@echo off
rem Builds the one-file Windows program (dist\YouTubeTranscriptTool.exe) from this folder.
rem GitHub builds the same file for every release - this is for building your own copy.
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run setup.bat first.
    pause
    exit /b 1
)
echo Installing the build tool (PyInstaller) ...
".venv\Scripts\python.exe" -m pip install --quiet --upgrade pyinstaller -r requirements.txt
if errorlevel 1 (
    echo Could not install PyInstaller - check your internet connection.
    pause
    exit /b 1
)
echo Building - this takes a minute or two ...
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean YouTubeTranscriptTool.spec
if errorlevel 1 (
    echo The build failed - see the messages above.
    pause
    exit /b 1
)
echo.
echo Done: %~dp0dist\YouTubeTranscriptTool.exe
echo Copy it into a folder of its own - it keeps config.toml and the output folder next to itself.
pause
