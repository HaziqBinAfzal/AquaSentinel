@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title AquaSentinel - Water Cyber Defense Workstation
chcp 65001 >nul 2>&1
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

cls
echo ========================================================================
echo                              AQUASENTINEL
echo                   WATER CYBER DEFENSE WORKSTATION
echo ========================================================================
echo.
echo   EVIDENCE-DRIVEN  ^|  LOCAL  ^|  READ-ONLY  ^|  SCHEMA-ADAPTIVE
echo   No PLC, SCADA, pump, valve or dosing-controller control connection.
echo.

set "PYTHON_CMD="
where py >nul 2>&1 && set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD where python >nul 2>&1 && set "PYTHON_CMD=python"
if not defined PYTHON_CMD (
  echo [FAIL] Python 3.10+ was not found.
  goto :fatal
)
%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 (
  echo [FAIL] AquaSentinel requires Python 3.10 or newer.
  goto :fatal
)
if not exist ".venv\Scripts\python.exe" (
  echo [SETUP] Creating isolated Python environment...
  %PYTHON_CMD% -m venv .venv
  if errorlevel 1 goto :fatal
)
set "VENV_PY=.venv\Scripts\python.exe"
"%VENV_PY%" -c "import aquasentinel, rich, sklearn, openpyxl, prometheus_client" >nul 2>&1
if errorlevel 1 (
  echo [SETUP] Installing AquaSentinel dependencies...
  "%VENV_PY%" -m pip install -e .
  if errorlevel 1 goto :fatal
)
"%VENV_PY%" -m aquasentinel --self-check >nul
if errorlevel 1 goto :fatal
echo [READY] AquaSentinel analysis engine online.

:menu
echo.
echo ------------------------------------------------------------------------
echo   [1] LOAD EVIDENCE + OPEN TERMINAL COMMAND CENTER
 echo   [2] COMMAND CENTER + LIVE GRAFANA MONITORING
 echo   [3] OPEN GRAFANA
 echo   [4] OPEN PROMETHEUS
 echo   [5] OPEN RAW METRICS
 echo   [6] SYSTEM DIAGNOSTICS
 echo   [7] ARCHITECTURE ^& ASSURANCE
 echo   [Q] QUIT
 echo ------------------------------------------------------------------------
choice /C 1234567Q /N /M "Select option: "
if errorlevel 8 exit /b 0
if errorlevel 7 goto :assurance
if errorlevel 6 goto :diagnostics
if errorlevel 5 goto :metrics
if errorlevel 4 goto :prometheus
if errorlevel 3 goto :grafana
if errorlevel 2 goto :monitoring
if errorlevel 1 goto :command
goto :menu

:collect
set "EVIDENCE_ARGS="
set /a COUNT=0
echo.
echo Supported evidence: CSV, JSON, JSONL, XLSX
 echo Enter one file or folder at a time. Drag-and-drop paths are supported.
 echo Press ENTER on an empty line when finished.
:collect_loop
set "ITEM="
set /p "ITEM=Evidence path: "
set "ITEM=!ITEM:"=!"
if not defined ITEM goto :collect_done
if not exist "!ITEM!" (
  echo [SKIP] Path not found: !ITEM!
  goto :collect_loop
)
set "EVIDENCE_ARGS=!EVIDENCE_ARGS! "!ITEM!""
set /a COUNT+=1
echo [ADDED] !ITEM!
goto :collect_loop
:collect_done
if !COUNT! EQU 0 (
  echo No evidence was selected.
  exit /b 1
)
echo [READY] !COUNT! evidence path(s) selected.
exit /b 0

:command
call :collect
if errorlevel 1 goto :menu
"%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --command-center
if errorlevel 1 goto :fatal
pause
goto :menu

:monitoring
call :collect
if errorlevel 1 goto :menu
where docker >nul 2>&1
if errorlevel 1 (
  echo [FAIL] Docker Desktop / Docker CLI was not found.
  goto :menu
)
echo.
echo [1/4] Starting AquaSentinel evidence metrics exporter...
start "AquaSentinel Metrics" /min cmd /c ""%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --monitor --metrics-port 9118"
timeout /t 2 /nobreak >nul
echo [2/4] Starting Prometheus + Grafana...
docker compose up -d
if errorlevel 1 (
  echo [FAIL] Monitoring containers could not start. Check Docker Desktop.
  goto :menu
)
echo [3/4] Waiting for local monitoring services...
timeout /t 5 /nobreak >nul
start "" http://localhost:3001/d/aquasentinel-main
start "" http://localhost:9118/metrics
echo [4/4] Opening evidence-driven Terminal Command Center...
echo.
echo Grafana:    http://localhost:3001/d/aquasentinel-main
 echo Prometheus: http://localhost:9091
 echo Metrics:    http://localhost:9118/metrics
 echo Login: admin / aquasentinel
 echo.
"%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --command-center
if errorlevel 1 goto :fatal
echo.
echo LIVE MONITORING ACTIVE. Review Grafana in your browser.
echo Press ENTER when you are finished with this monitoring session.
set /p "STOPSESSION="
echo Stopping local monitoring services...
docker compose down >nul 2>&1
taskkill /FI "WINDOWTITLE eq AquaSentinel Metrics" /T /F >nul 2>&1
echo [STOPPED] Monitoring session closed cleanly.
goto :menu

:grafana
start "" http://localhost:3001/d/aquasentinel-main
goto :menu
:prometheus
start "" http://localhost:9091
goto :menu
:metrics
start "" http://localhost:9118/metrics
goto :menu
:diagnostics
"%VENV_PY%" -m aquasentinel --self-check
"%VENV_PY%" -m aquasentinel doctor
where docker >nul 2>&1 && docker compose ps
pause
goto :menu
:assurance
"%VENV_PY%" -m aquasentinel --architecture
"%VENV_PY%" -m aquasentinel --compliance
pause
goto :menu
:fatal
echo.
echo ========================================================================
echo                         AQUASENTINEL STARTUP FAILED
echo ========================================================================
echo Review the message above. No industrial infrastructure was contacted.
pause
exit /b 1
