@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title AquaSentinel AI - One File Launcher

rem Force UTF-8 for Rich terminal output on Windows Command Prompt.
chcp 65001 >nul 2>&1
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "CHECK_ONLY=0"
if /I "%~1"=="--check-only" set "CHECK_ONLY=1"

cls
echo ================================================================
echo                    AQUASENTINEL AI v1.0.0
echo        Smart Water ^& Desalination Security Platform
echo ================================================================
echo.
echo SYNTHETIC - DEFENSIVE - READ ONLY CLASSROOM LAB
echo No real PLC, SCADA, dosing controller or water utility connection.
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
echo [8/8] Running functional smoke checks...
"%VENV_PY%" -m aquasentinel architecture >nul
if errorlevel 1 goto :fatal
"%VENV_PY%" -m aquasentinel run --scenario normal --samples 1 >nul
if errorlevel 1 goto :fatal
"%VENV_PY%" -m aquasentinel run --scenario dosing_event --samples 1 >nul
if errorlevel 1 goto :fatal
"%VENV_PY%" -m aquasentinel incident --scenario dosing_event --step 8 >nul
if errorlevel 1 goto :fatal
"%VENV_PY%" -m aquasentinel report --output reports\launcher_preflight_report.json >nul
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

echo AquaSentinel is ready. Starting the guided Topic 133 demonstration...
echo Press Ctrl+C at any time if you need to stop the demo.
echo.
timeout /t 2 /nobreak >nul

"%VENV_PY%" -m aquasentinel exam-demo
if errorlevel 1 goto :fatal

echo.
echo ================================================================
echo                       DEMO COMPLETE
echo ================================================================
echo.
echo Optional next command for the live industrial SOC dashboard:
echo   .venv\Scripts\python.exe -m aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
echo.
pause
exit /b 0

:fatal
echo.
echo ================================================================
echo                    AQUASENTINEL CHECK FAILED
echo ================================================================
echo One of the setup or verification stages failed.
echo Read the error shown above, fix it, then double-click AquaSentinel.bat again.
echo No real infrastructure was contacted or modified.
echo.
if "%CHECK_ONLY%"=="1" exit /b 1
pause
exit /b 1
