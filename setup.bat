@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title YouTube Transcript Tool - setup
echo.
echo  === YouTube Transcript Tool - one-time setup ===
echo.

rem ---- find Python 3.11 or newer (yt-dlp needs it) ------------------------------
set "PY="
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
    if errorlevel 1 (
        echo  The existing .venv uses an old Python - rebuilding it.
        rmdir /s /q ".venv"
    )
)
where py >nul 2>nul
if errorlevel 1 goto :trypython
for %%V in (3.14 3.13 3.12 3.11 3) do (
    if not defined PY (
        py -%%V -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
        if not errorlevel 1 set "PY=py -%%V"
    )
)
:trypython
if defined PY goto :havepython
for %%P in (python python3) do (
    if not defined PY (
        %%P -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
        if not errorlevel 1 set "PY=%%P"
    )
)
if not defined PY goto :nopython
:havepython
echo  Using Python: %PY%

rem ---- private environment so nothing else on the PC is affected -------------
if not exist ".venv\Scripts\python.exe" (
    echo  Creating a private Python environment in .venv ...
    %PY% -m venv .venv
    if errorlevel 1 goto :venvfail
)

echo  Installing / updating required packages ...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install --upgrade -r requirements.txt
if errorlevel 1 goto :pipfail
rem optional: lets yt-dlp fetch captions the way a browser does (helps against blocking)
".venv\Scripts\python.exe" -m pip install --upgrade "yt-dlp[curl-cffi]" --quiet >nul 2>nul
if errorlevel 1 echo  (optional curl_cffi helper could not be installed - that's OK)

rem ---- Deno: the JavaScript runtime yt-dlp uses for YouTube ------------------
where deno >nul 2>nul
if not errorlevel 1 goto :denook
if exist "%LOCALAPPDATA%\Microsoft\WinGet\Links\deno.exe" goto :denook
if exist "%USERPROFILE%\.deno\bin\deno.exe" goto :denook
echo.
echo  yt-dlp works best with Deno, a small JavaScript runtime, installed.
choice /c YN /m "  Install Deno now with winget"
if errorlevel 2 goto :denoskip
winget install --id DenoLand.Deno -e
goto :denodone
:denoskip
echo  Skipped. You can install it later with:  winget install DenoLand.Deno
goto :denodone
:denook
echo  Deno is installed.
:denodone

rem ---- config -------------------------------------------------------------------
if not exist "config.toml" (
    copy /y "config.example.toml" "config.toml" >nul
    echo  Created config.toml - open it in Notepad to set your keywords.
)

rem ---- optional Desktop shortcut to the window interface -------------------------
powershell -NoProfile -Command "exit [int](-not (Test-Path ([Environment]::GetFolderPath('Desktop') + '\YouTube Transcript Tool.lnk')))" >nul 2>nul
if not errorlevel 1 goto :shortcutdone
echo.
choice /c YN /m "  Put a 'YouTube Transcript Tool' shortcut on your Desktop"
if errorlevel 2 goto :shortcutdone
set "TOOLDIR=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d=$env:TOOLDIR; $s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop') + '\YouTube Transcript Tool.lnk'); $s.TargetPath=(Join-Path $d 'gui.bat'); $s.WorkingDirectory=$d; $s.WindowStyle=7; $s.Description='Search YouTube and download transcripts'; $s.Save()" >nul 2>nul
if errorlevel 1 (echo  Could not create the shortcut - you can still double-click gui.bat.) else (echo  Shortcut created on your Desktop.)
:shortcutdone

echo.
echo  Running a quick self-test ...
".venv\Scripts\python.exe" yt.py doctor
echo.
echo  Setup finished. Next: edit config.toml, then double-click run.bat (or gui.bat).
pause
exit /b 0

:nopython
rem a per-user install from an earlier attempt may not be on PATH in this window yet
for %%V in (314 313 312 311) do (
    if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" set PY="%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe"
)
if defined PY goto :havepython
echo  Could not find Python 3.11 or newer on this PC.
where winget >nul 2>nul
if errorlevel 1 goto :nopython_manual
choice /c YN /m "  Install Python 3.13 now with winget (free, from python.org)"
if errorlevel 2 goto :nopython_manual
winget install --id Python.Python.3.13 -e --scope user --accept-package-agreements --accept-source-agreements
if errorlevel 1 if not exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" goto :nopython_manual
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PY="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto :havepython
)
echo  Python was installed but this window cannot see it yet - close it and run setup.bat again.
pause
exit /b 1

:nopython_manual
echo  Install it from https://www.python.org/downloads/  and tick "Add python.exe to PATH",
echo  or run:  winget install Python.Python.3.13
echo  then run setup.bat again.
pause
exit /b 1

:venvfail
echo  Could not create the .venv environment.
pause
exit /b 1

:pipfail
echo  Package installation failed - check your internet connection and run setup.bat again.
pause
exit /b 1
