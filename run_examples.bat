@echo off
call .\activate.bat

setlocal enabledelayedexpansion

SET SCRIPT_DIR=%~dp0
SET PYTHONPATH=%SCRIPT_DIR%

echo Running all Python examples recursively from the "examples/" folder...

rem Traverse the examples directory recursively and run each .py file
for /r "examples" %%f in (*.py) do (
    echo Running: %%f
    python "%%f"
    if errorlevel 1 (
        echo ERROR - %%f
        exit /b 1
    )
)

echo " "
echo " "
echo Examples finished - SUCESSFULLY
echo " "
echo " "
