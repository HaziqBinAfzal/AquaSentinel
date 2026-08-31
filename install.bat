@echo off
setlocal

where py >nul 2>nul
if %errorlevel%==0 (
  set PYTHON_CMD=py -3
) else (
  set PYTHON_CMD=python
)

%PYTHON_CMD% -m venv .venv
if errorlevel 1 exit /b 1

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

pip install -e .
if errorlevel 1 exit /b 1

aquasentinel doctor
if errorlevel 1 exit /b 1

echo.
echo AquaSentinel installed successfully.
echo Activate later with: .venv\Scripts\activate
echo Start the exam dashboard with: aquasentinel live --scenario normal
endlocal
