@echo off
rem Removes the daily scheduled task created by schedule_daily.bat.
schtasks /Delete /F /TN "YouTube Transcript Tool"
pause
