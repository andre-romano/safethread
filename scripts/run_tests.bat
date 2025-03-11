@echo off
call .\scripts\activate.bat

SET SCRIPT_DIR=%~dp0
SET PYTHONPATH=%SCRIPT_DIR%

echo Running tests ...
@REM python -m unittest discover tests
pytest -x tests/