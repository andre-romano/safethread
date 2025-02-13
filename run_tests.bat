@echo off
call .\activate.bat

SET SCRIPT_DIR=%~dp0
SET PYTHONPATH=%SCRIPT_DIR%

echo 1) Installing pytest ...
pip3 install pytest

echo 2) Running tests ...
@REM python -m unittest discover tests
pytest tests/