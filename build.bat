
@echo off
call .\activate.bat

echo Installing build system
python3 -m pip install --upgrade build twine

echo Building ...
python3 -m build