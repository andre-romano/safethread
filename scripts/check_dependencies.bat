@echo off
call .\scripts\activate.bat

SET SCRIPT_DIR=%~dp0
SET PYTHONPATH=%SCRIPT_DIR%

echo Running dependencies check ...
pydeps ./safethread/

