@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title AquaSentinel AI - Local Analysis Workstation

rem UTF-8 support for Rich terminal output on Windows Command Prompt.
chcp 65001 >nul 2>&1
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "CHECK_ONLY=0"
if /I "%~1"=="--check-only" set "CHECK_ONLY=1"

cls
echo ================================================================
echo                    AQUASENTINEL AI v1.0.0
echo              Local Water / OT Analysis Workstation
echo ================================================================
echo.
echo DEFENSIVE - LOCAL - READ ONLY
echo AquaSentinel analyzes files you provide. No dataset is preloaded.
echo No PLC, SCADA, dosing controller or utility control connection.
echo.

set "PYTHON_CMD="
where py >nul 2>&1 && set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD where python >nul 2>&1 && set "PYTHON_CMD=python"

if not defined PYTHON_CMD (
    echo [FAIL] Python 3 was not found.
    echo Install Python 3.10 or newer, then run this file again.
    goto :fatal
)

echo [1/8] Python detected
%PYTHON_CMD% --version
if errorlevel 1 goto :fatal
%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 (
    echo [FAIL] AquaSentinel requires Python 3.10 or newer.
    goto :fatal
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [2/8] Creating isolated AquaSentinel environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :fatal
) else (
    echo.
    echo [2/8] Existing AquaSentinel environment found
)

set "VENV_PY=.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo [FAIL] Virtual environment was not created correctly.
    goto :fatal
)

echo.
echo [3/8] Preparing package tools...
"%VENV_PY%" -m pip install --upgrade pip >nul
if errorlevel 1 goto :fatal

echo.
echo [4/8] Installing AquaSentinel and verification tools...
"%VENV_PY%" -m pip install -e ".[dev]"
if errorlevel 1 goto :fatal

echo.
echo [5/8] Running environment and safety checks...
"%VENV_PY%" -m aquasentinel doctor
if errorlevel 1 goto :fatal

echo.
echo [6/8] Running project tests...
"%VENV_PY%" -m pytest -q
if errorlevel 1 goto :fatal

echo.
echo [7/8] Running code-quality and defensive security checks...
"%VENV_PY%" -m ruff check aquasentinel tests
if errorlevel 1 goto :fatal
"%VENV_PY%" -m bandit -q -r aquasentinel
if errorlevel 1 goto :fatal

echo.
echo [8/8] Running local-analysis smoke checks...
"%VENV_PY%" -m aquasentinel architecture >nul
if errorlevel 1 goto :fatal
"%VENV_PY%" -m aquasentinel analyze --check-only >nul
if errorlevel 1 goto :fatal
"%VENV_PY%" -m aquasentinel web --check-only >nul
if errorlevel 1 goto :fatal

echo.
echo ================================================================
echo                    ALL CHECKS PASSED
echo ================================================================
echo.

if "%CHECK_ONLY%"=="1" (
    echo Windows launcher verification complete.
    exit /b 0
)

:menu
echo Choose how you want to use AquaSentinel:
echo.
echo   [1] Browser interface - select and analyze a file in localhost
 echo   [2] Terminal interface - enter a local file path
 echo   [Q] Quit
 echo.
choice /C 12Q /N /M "Select option [1/2/Q]: "
if errorlevel 3 exit /b 0
if errorlevel 2 goto :terminal
if errorlevel 1 goto :browser

goto :menu

:browser
echo.
echo Starting local browser interface...
echo URL: http://127.0.0.1:8765/
echo Select a .log, .txt, .csv, .json or .jsonl file in the page.
echo Keep this terminal open. Press Ctrl+C here to stop the local server.
echo.
"%VENV_PY%" -m aquasentinel web --port 8765
if errorlevel 1 goto :fatal
exit /b 0

:terminal
echo.
echo Supported files: .log .txt .csv .json .jsonl
set "DATA_FILE="
set /p "DATA_FILE=Enter or paste the full file path: "
set "DATA_FILE=!DATA_FILE:"=!"
if not defined DATA_FILE (
    echo No file was entered.
    goto :menu
)
if not exist "!DATA_FILE!" (
    echo [FAIL] File not found: !DATA_FILE!
    goto :menu
)
echo.
"%VENV_PY%" -m aquasentinel analyze "!DATA_FILE!"
if errorlevel 1 goto :fatal
echo.
pause
goto :menu

:fatal
echo.
echo ================================================================
echo                    AQUASENTINEL CHECK FAILED
echo ================================================================
echo One of the setup, verification or analysis stages failed.
echo Review the error above and try again.
echo No industrial infrastructure was contacted or modified.
echo.
if "%CHECK_ONLY%"=="1" exit /b 1
pause
exit /b 1
