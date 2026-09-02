@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title AquaSentinel - Water Security and Resilience Workstation
chcp 65001 >nul 2>&1
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cls
echo ========================================================================
echo                              AQUASENTINEL
echo                 WATER SECURITY ^& RESILIENCE WORKSTATION
echo ========================================================================
echo   EVIDENCE-DRIVEN ^| LOCAL ^| READ-ONLY ^| SCHEMA-ADAPTIVE ^| HUMAN REVIEW
echo   No PLC, SCADA, pump, valve or dosing-controller control connection.
echo.
set "PYTHON_CMD="
where py >nul 2>&1 && set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD where python >nul 2>&1 && set "PYTHON_CMD=python"
if not defined PYTHON_CMD (echo [FAIL] Python 3.10+ was not found.&goto :fatal)
%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 (echo [FAIL] AquaSentinel requires Python 3.10 or newer.&goto :fatal)
if not exist ".venv\Scripts\python.exe" (%PYTHON_CMD% -m venv .venv || goto :fatal)
set "VENV_PY=.venv\Scripts\python.exe"
"%VENV_PY%" -c "import aquasentinel, rich, sklearn, openpyxl, prometheus_client, flask" >nul 2>&1
if errorlevel 1 (echo [SETUP] Installing AquaSentinel dependencies...&"%VENV_PY%" -m pip install -e . || goto :fatal)
"%VENV_PY%" -m aquasentinel --self-check >nul || goto :fatal
echo [READY] AquaSentinel analysis engine online.
:menu
echo.
echo ------------------------------------------------------------------------
echo   [1] LOAD EVIDENCE + TERMINAL COMMAND CENTER
 echo   [2] COMMAND CENTER + LIVE GRAFANA MONITORING
 echo   [3] ANALYZE EVIDENCE + EXPORT ASSURANCE REPORT
 echo   [4] OPEN GRAFANA
 echo   [5] OPEN PROMETHEUS
 echo   [6] OPEN RAW METRICS
 echo   [7] SYSTEM DIAGNOSTICS
 echo   [8] ARCHITECTURE ^& ASSURANCE
 echo   [9] WEB EVIDENCE WORKSTATION
 echo   [Q] QUIT
 echo ------------------------------------------------------------------------
choice /C 123456789Q /N /M "Select option: "
if errorlevel 10 exit /b 0
if errorlevel 9 goto :web
if errorlevel 8 goto :assurance
if errorlevel 7 goto :diagnostics
if errorlevel 6 goto :metrics
if errorlevel 5 goto :prometheus
if errorlevel 4 goto :grafana
if errorlevel 3 goto :report
if errorlevel 2 goto :monitoring
if errorlevel 1 goto :command
goto :menu
:collect
set "EVIDENCE_ARGS="
set /a COUNT=0
echo Supported evidence: CSV, JSON, JSONL, XLSX
echo Enter one file or folder at a time. Drag-and-drop paths are supported.
echo Press ENTER on an empty line when finished.
:collect_loop
set "ITEM="
set /p "ITEM=Evidence path: "
if not defined ITEM goto :collect_done
for %%A in ("!ITEM!") do set "ITEM=%%~A"
if not exist "!ITEM!" (echo [SKIP] Path not found: !ITEM!&goto :collect_loop)
set "EVIDENCE_ARGS=!EVIDENCE_ARGS! "!ITEM!""
set /a COUNT+=1
echo [ADDED] !ITEM!
goto :collect_loop
:collect_done
if !COUNT! EQU 0 (echo No evidence was selected.&exit /b 1)
echo [READY] !COUNT! evidence path(s) selected.&exit /b 0
:command
call :collect
if errorlevel 1 goto :menu
"%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --command-center || goto :fatal
pause&goto :menu
:report
call :collect
if errorlevel 1 goto :menu
if not exist "reports" mkdir "reports"
for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "STAMP=%%T"
set "REPORT_PATH=reports\AquaSentinel-Evidence-Report-!STAMP!.md"
"%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --command-center --report "!REPORT_PATH!" || goto :fatal
echo.
echo [EXPORTED] !REPORT_PATH!
start "" notepad "!REPORT_PATH!"
pause&goto :menu
:monitoring
call :collect
if errorlevel 1 goto :menu
where docker >nul 2>&1
if errorlevel 1 (echo [FAIL] Docker Desktop / Docker CLI was not found.&goto :menu)
start "AquaSentinel Metrics" /min cmd /c ""%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --monitor --metrics-port 9118"
timeout /t 2 /nobreak >nul
docker compose up -d || goto :menu
timeout /t 5 /nobreak >nul
start "" http://localhost:3001/d/aquasentinel-main
"%VENV_PY%" -m aquasentinel --files !EVIDENCE_ARGS! --command-center || goto :fatal
echo Grafana http://localhost:3001/d/aquasentinel-main ^| Prometheus http://localhost:9091 ^| Metrics http://localhost:9118/metrics
echo Login: admin / aquasentinel
echo Press ENTER when finished with this monitoring session.
set /p "STOPSESSION="
docker compose down >nul 2>&1
taskkill /FI "WINDOWTITLE eq AquaSentinel Metrics" /T /F >nul 2>&1
echo [STOPPED] Monitoring session closed cleanly.&goto :menu
:web
echo [WEB] Starting local AquaSentinel browser workstation...
echo [WEB] Uploads are analyzed locally and removed after each request.
"%VENV_PY%" -m aquasentinel.webapp
if errorlevel 1 goto :fatal
goto :menu
:grafana
start "" http://localhost:3001/d/aquasentinel-main&goto :menu
:prometheus
start "" http://localhost:9091&goto :menu
:metrics
start "" http://localhost:9118/metrics&goto :menu
:diagnostics
"%VENV_PY%" -m aquasentinel --self-check
where docker >nul 2>&1 && docker compose ps
pause&goto :menu
:assurance
"%VENV_PY%" -m aquasentinel --architecture
"%VENV_PY%" -m aquasentinel --compliance
pause&goto :menu
:fatal
echo.
echo ======================= AQUASENTINEL STARTUP FAILED ======================
echo Review the message above. No industrial infrastructure was contacted.
pause&exit /b 1
