@echo off
call .\activate.bat

SET SCRIPT_DIR=%~dp0
SET PYTHONPATH=%SCRIPT_DIR%

echo %PYTHONPATH%

echo "Installing unit test dependencies ..."
pip3 install pytest

echo "Running tests ..."
@REM python -m unittest discover tests
pytest tests/