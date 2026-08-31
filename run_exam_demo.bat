@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo AquaSentinel virtual environment not found.
  echo Run install.bat first.
  pause
  exit /b 1
)

call ".venv\Scripts\activate.bat"
cls
echo Starting AquaSentinel AI guided Topic 133 exam demo...
echo.
aquasentinel exam-demo

echo.
echo Demo finished. Press any key to close.
pause >nul
