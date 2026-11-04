@echo off
setlocal
rem Creates a Windows scheduled task that runs the tool once a day with your config.toml.
rem Remove it again with unschedule.bat.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run setup.bat first.
    pause
    exit /b 1
)
echo.
echo  This creates a daily Windows scheduled task named "YouTube Transcript Tool"
echo  that searches with your config.toml and downloads any new transcripts.
echo  It runs while you are logged in. Output is logged to output\scheduled_runs.log
echo.
set "RUNAT="
set /p "RUNAT=  What time each day? (24-hour HH:MM, Enter = 08:00): "
if defined RUNAT set "RUNAT=%RUNAT: =%"
if not defined RUNAT set "RUNAT=08:00"
rem schtasks wants HH:MM - turn 7:45 into 07:45
if "%RUNAT:~1,1%"==":" set "RUNAT=0%RUNAT%"
set "SCRIPT=%~dp0run_scheduled.bat"
rem PowerShell's version can also run on battery and catch up a run missed while the PC was off/asleep
powershell -NoProfile -ExecutionPolicy Bypass -Command "$a = New-ScheduledTaskAction -Execute ([char]34 + $env:SCRIPT + [char]34) -WorkingDirectory (Split-Path $env:SCRIPT); $t = New-ScheduledTaskTrigger -Daily -At $env:RUNAT; $s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 8); Register-ScheduledTask -TaskName 'YouTube Transcript Tool' -Action $a -Trigger $t -Settings $s -Force -ErrorAction Stop | Out-Null" >nul 2>nul
if not errorlevel 1 goto :created
schtasks /Create /F /SC DAILY /ST %RUNAT% /TN "YouTube Transcript Tool" /TR "\"%SCRIPT%\""
if errorlevel 1 (
    echo.
    echo  Could not create the task. Check the time format, e.g. 07:30
    pause
    exit /b 1
)
:created
echo.
echo  Done. It will run every day at %RUNAT%. To run it right now:  schtasks /Run /TN "YouTube Transcript Tool"
pause
