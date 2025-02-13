@echo off
setlocal enabledelayedexpansion

set "version="
for /f "tokens=2 delims==," %%a in ('findstr "version=" setup.py') do (
    set "line=%%a"
    set "line=!line:~1,-1!"
    set "version=!line!"
)

echo v%version%
