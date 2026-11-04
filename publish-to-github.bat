@echo off
rem Publish this folder to GitHub in one double-click: commit everything that changed, then push.
rem Your own settings (config.toml with proxy passwords and API key), cookies, proxy lists and the
rem output folder are never published - see .gitignore.
setlocal EnableExtensions
cd /d "%~dp0"
title Publish YouTube Transcript Tool to GitHub
set "REPO_URL=https://github.com/austin-72/YouTubeTranscriptTool.git"
set "REPO_PAGE=https://github.com/austin-72/YouTubeTranscriptTool"
set "BRANCH=main"

rem ======================= COMMIT MESSAGE =======================
rem Updated together with every new version of the tool.
set "MSG_FILE=%TEMP%\ytt_commit_message.txt"
>"%MSG_FILE%" echo v1.1.1: publish script, README screenshots and AI use cases
>>"%MSG_FILE%" echo.
>>"%MSG_FILE%" echo - publish-to-github.bat: commit and push this folder in one double-click
>>"%MSG_FILE%" echo - .gitignore keeps config.toml, cookies, proxy lists and output private
>>"%MSG_FILE%" echo - README: screenshots of the window, the dialogs and the video list
>>"%MSG_FILE%" echo - README: how to use the transcripts with AI tools, with example prompts
rem ===================== END COMMIT MESSAGE =====================

rem ---- find git (install it if missing) -------------------------------------------------------
where git >nul 2>&1
if not errorlevel 1 goto have_git
if exist "%ProgramFiles%\Git\cmd\git.exe" (
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
    goto have_git
)
echo Git is not installed. It's needed to publish to GitHub.
where winget >nul 2>&1
if errorlevel 1 goto no_git
choice /c YN /m "Install Git now (free, from git-scm.com via winget)"
if errorlevel 2 goto no_git
winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
if exist "%ProgramFiles%\Git\cmd\git.exe" (
    set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
    goto have_git
)
:no_git
echo.
echo Please install Git from https://git-scm.com/download/win and run this file again.
goto fail

:have_git
rem ---- first time in this folder: connect it to the GitHub repository -------------------------
if exist ".git" goto have_repo
echo Connecting this folder to %REPO_PAGE% ...
git init -q
if errorlevel 1 goto fail
git symbolic-ref HEAD refs/heads/%BRANCH%
git remote add origin "%REPO_URL%"
git ls-remote --exit-code --heads origin %BRANCH% >nul 2>&1
if errorlevel 128 goto fetch_failed
if errorlevel 2 goto have_repo
rem GitHub already has the project: build on its history, keeping the files in this folder as they are
git fetch -q origin %BRANCH%
if errorlevel 1 goto fetch_failed
git reset -q origin/%BRANCH%
if errorlevel 1 goto fail

:have_repo
git remote get-url origin >nul 2>&1
if errorlevel 1 git remote add origin "%REPO_URL%"

rem ---- who you are (shown on GitHub as the author of the commit) ---------------------------------
set "GIT_EMAIL="
for /f "delims=" %%a in ('git config user.email 2^>nul') do set "GIT_EMAIL=%%a"
if defined GIT_EMAIL goto have_identity
echo.
echo Git needs your name and e-mail for the commit (use the e-mail of your GitHub account,
echo or the "noreply" address from github.com/settings/emails to keep yours private).
set "GIT_NAME="
set /p "GIT_NAME=Your name: "
set /p "GIT_EMAIL=Your e-mail: "
if not defined GIT_EMAIL goto fail
git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"
:have_identity

rem ---- never publish private files, even if they were added before --------------------------------
git rm -q -r --cached --ignore-unmatch config.toml proxies.txt keywords.txt output .venv >nul 2>&1

rem ---- the commit message ---------------------------------------------------------------------------
echo.
echo Commit message:
echo ------------------------------------------------------------
type "%MSG_FILE%"
echo ------------------------------------------------------------
set "CUSTOM="
set /p "CUSTOM=Press Enter to use it, or type your own one-line message: "
if not defined CUSTOM goto message_done
rem (a message of 3+ characters replaces the prepared one; ! keeps special characters like & safe)
setlocal EnableDelayedExpansion
set "USE_CUSTOM="
if not "!CUSTOM!"=="" if not "!CUSTOM:~2!"=="" set "USE_CUSTOM=1"
if defined USE_CUSTOM >"%MSG_FILE%" echo.!CUSTOM!
endlocal
:message_done

rem ---- commit -----------------------------------------------------------------------------------------
git add -A
if errorlevel 1 goto fail
set "PRIVATE="
for /f "delims=" %%f in ('git diff --cached --name-only --diff-filter^=AM -- config.toml proxies.txt keywords.txt output .venv ":(glob)**/*cookies*"') do set "PRIVATE=%%f"
if defined PRIVATE (
    echo.
    echo STOPPED: a private file was about to be published ^(config.toml, cookies, proxies or output^).
    echo Nothing was sent. Check .gitignore in this folder.
    git reset -q
    goto fail
)
git diff --cached --quiet
if not errorlevel 1 (
    echo.
    echo No changes since the last commit.
    goto push
)
git commit -q -F "%MSG_FILE%"
if errorlevel 1 goto fail
echo Committed.

:push
rem ---- bring in anything that's newer on GitHub, then send ------------------------------------------
git ls-remote --exit-code --heads origin %BRANCH% >nul 2>&1
if errorlevel 128 goto fetch_failed
if errorlevel 2 goto do_push
git pull -q --rebase origin %BRANCH%
if errorlevel 1 (
    git rebase --abort >nul 2>&1
    echo.
    echo GitHub has changes that clash with the ones in this folder ^(someone edited the same lines
    echo on github.com^). Nothing was sent. Open the folder in GitHub Desktop to sort it out.
    goto fail
)
:do_push
echo Sending to GitHub ^(the first time, a browser window asks you to sign in^) ...
git push -u origin %BRANCH%
if errorlevel 1 (
    echo.
    echo The push failed. Check that you're signed in to the GitHub account that owns
    echo %REPO_PAGE% and try again.
    goto fail
)
echo.
echo Published: %REPO_PAGE%
del "%MSG_FILE%" >nul 2>&1
choice /c YN /t 15 /d N /m "Open the GitHub page"
if errorlevel 2 goto end
start "" "%REPO_PAGE%"
goto end

:fetch_failed
echo Could not download the project's history from GitHub - check your internet connection.
:fail
echo.
echo Not published.
pause
exit /b 1

:end
endlocal
exit /b 0
