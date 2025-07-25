@echo off
setlocal enabledelayedexpansion

set GAME_FOLDER=REPO
set GAME_EXECUTABLE=REPO.exe

REM python -m pip install --quiet --upgrade psutil
REM python -m pip install --quiet psutil==7.0.0
python -c "import psutil" 2>NUL || python -m pip install --quiet psutil==7.0.0

set PYTHON_SCRIPT=%REPO_PYSCRIPT%

REM set your path to the Steam Library
set STEAM1=%ProgramFiles(x86)%\Steam\steamapps\common\%GAME_FOLDER%
set STEAM2=D:\SteamLibrary\steamapps\common\%GAME_FOLDER%
set STEAM3=E:\Games\SteamLibrary\steamapps\common\%GAME_FOLDER%

set FOUND_PATH=

if exist "%STEAM1%" set FOUND_PATH=%STEAM1%
if exist "%STEAM2%" set FOUND_PATH=%STEAM2%
if exist "%STEAM3%" set FOUND_PATH=%STEAM3%

if not defined FOUND_PATH (
    echo [ERROR] Game REPO not found in known locations.
    pause
    exit /b
)

echo [INFO] Game found at: %FOUND_PATH%

echo [INFO] Running copying script...
start "" python "%PYTHON_SCRIPT%"

echo [INFO] Launching REPO...
start "" "%FOUND_PATH%\%GAME_EXECUTABLE%"

pause