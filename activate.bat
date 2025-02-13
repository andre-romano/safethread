@echo off

:: Get the full script directory path
set SCRIPT_PATH=%~dp0

:: Path to your virtual environment
set VENV_PATH="%SCRIPT_PATH%venv"

:: Check if the venv folder exists
if not exist "%VENV_PATH%" (
    echo Virtual environment not found. Creating a new one...
    python -m venv "%VENV_PATH%"
)

:: Activate the virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

:: Test environment active
if defined VIRTUAL_ENV (
    echo Virtual environment is active at: %VIRTUAL_ENV%
) else (
    echo No active virtual environment found.   
    pause 
)
python -V
