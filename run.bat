@echo off
setlocal
cd /d "%~dp0"
title Income Video Engine
if not exist venv\Scripts\python.exe (
  echo Please run install.bat first.
  pause & exit /b 1
)
echo ==============================================
echo   Income Video Engine
echo ==============================================
set SCRIPT=
set AUDIO=
set MODE=
set SEED=1
set /p SCRIPT=Drag your script .txt file here and press Enter: 
set SCRIPT=%SCRIPT:"=%
set /p AUDIO=Drag your narration audio here (or just press Enter to use the AI voice): 
set /p MODE=Type P = quick 720p test,  H = HD 1080p 30fps,  F = BEST 1080p 60fps (slow),  U = 1440p 60fps : 
set /p SEED=Edit style number (1,2,3... different number = different edit) [1]: 
if "%SEED%"=="" set SEED=1
set ARGS=--seed %SEED%
if /i "%MODE%"=="P" set ARGS=%ARGS% --quality preview
if /i "%MODE%"=="H" set ARGS=%ARGS% --quality hd
if /i "%MODE%"=="U" set ARGS=%ARGS% --quality uhd
if defined AUDIO (
  set AUDIO=%AUDIO:"=%
  set ARGS=%ARGS% --audio "%AUDIO%"
)
venv\Scripts\python.exe main.py "%SCRIPT%" %ARGS%
echo.
echo Finished. Your video is in the "output" folder.
explorer output
pause
