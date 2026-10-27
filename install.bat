@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Income Video Engine - Installer
echo ==============================================
echo   Income Video Engine - one click installer
echo ==============================================
echo.

rem ---------- 1. Python ----------
set PY=
where py >nul 2>&1 && ( py -3 --version >nul 2>&1 && set PY=py -3 )
if not defined PY ( where python >nul 2>&1 && ( python --version >nul 2>&1 && set PY=python ) )
if not defined PY (
  echo [1/4] Python not found. Installing Python 3.12 with winget ...
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  if exist "%LocalAppData%\Programs\Python\Python312\python.exe" set PY="%LocalAppData%\Programs\Python\Python312\python.exe"
)
if not defined PY (
  echo.
  echo [ERROR] Could not install Python automatically.
  echo Install Python 3.10+ from https://www.python.org/downloads/  ^(tick "Add python.exe to PATH"^)
  echo then run install.bat again.
  pause & exit /b 1
)
echo [1/4] Python OK: %PY%

rem ---------- 2. FFmpeg ----------
set FF=
where ffmpeg >nul 2>&1 && set FF=1
if not defined FF ( for /f %%F in ('dir /s /b "tools\ffmpeg.exe" 2^>nul') do set FF=1 )
if not defined FF (
  echo [2/4] Downloading FFmpeg ^(about 90 MB^) ...
  if not exist tools mkdir tools
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'tools\ffmpeg.zip'; Expand-Archive -Force 'tools\ffmpeg.zip' 'tools\ffmpeg'; Remove-Item 'tools\ffmpeg.zip'"
  for /f %%F in ('dir /s /b "tools\ffmpeg.exe" 2^>nul') do set FF=1
)
if not defined FF (
  echo [ERROR] FFmpeg download failed. Check your internet and run install.bat again.
  pause & exit /b 1
)
echo [2/4] FFmpeg OK

rem ---------- 3. Python packages ----------
echo [3/4] Creating environment and installing packages ^(a few minutes^) ...
if not exist venv\Scripts\python.exe ( %PY% -m venv venv )
if not exist venv\Scripts\python.exe ( echo [ERROR] Could not create venv & pause & exit /b 1 )
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 ( echo [ERROR] Package install failed. Check your internet and run install.bat again. & pause & exit /b 1 )

rem ---------- 4. Assets ----------
echo [4/4] Creating sound effects ...
venv\Scripts\python.exe make_assets.py
if not exist output mkdir output

echo.
echo ==============================================
echo   INSTALL COMPLETE
echo   Now double-click  run.bat  to make a video.
echo ==============================================
set /p SAMPLE=Render the sample video now? (Y/N): 
if /i "%SAMPLE%"=="Y" (
  venv\Scripts\python.exe main.py samples\income_plans.txt --preview
  if exist output explorer output
)
pause
