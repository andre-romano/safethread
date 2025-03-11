@echo off
setlocal enabledelayedexpansion
call .\scripts\activate.bat

echo ---- GENERATING NEW VERSION ----

echo 1) Checking VERSION file ...

:v_confirm
set "VERSION="
for /f "delims=" %%a in (VERSION) do set "VERSION=%%a"
echo VERSION = %VERSION%
set /p "CONFIRM=Version is correct? (y/n/t): "
if /i "%CONFIRM%"=="y" goto v_continue
if /i "%CONFIRM%"=="n" goto v_confirm
if /i "%CONFIRM%"=="t" goto cancel
echo Invalid option. Please, answer with y , n or t.
goto v_confirm

:v_continue

:b_confirm
echo 2) Building dist/ ...
call .\scripts\build.bat
set /p "CONFIRM=Building finished correctly? (y/n/t): "
if /i "%CONFIRM%"=="y" goto b_continue
if /i "%CONFIRM%"=="n" goto b_confirm
if /i "%CONFIRM%"=="t" goto cancel
echo Invalid option. Please, answer with y , n or t.
goto b_confirm

:b_continue

echo 3) Generating CHANGELOG.md ...
python ./scripts/gen_changelog.py

echo 4) Generating DOCS/ ...
python ./scripts/gen_docs.py

git status
pause

echo 5) Commiting in Github ...
git add .
git commit -m "release version v%VERSION%"
git tag v%VERSION%
git push --all
git push --tags

:c_confirm
set /p "CONFIRM=Commit finished correctly? (y/n/t): "
if /i "%CONFIRM%"=="y" goto c_continue
if /i "%CONFIRM%"=="n" goto cancel
if /i "%CONFIRM%"=="t" goto cancel
echo Invalid option. Please, answer with y , n or t.
goto c_confirm

:c_continue

:p_confirm
echo 5) Publishing in PyPi ...
twine upload dist/*
set /p "CONFIRM=Publishing finished correctly? (y/n/t): "
if /i "%CONFIRM%"=="y" goto p_continue
if /i "%CONFIRM%"=="n" goto p_confirm
if /i "%CONFIRM%"=="t" goto cancel
echo Invalid option. Please, answer with y , n or t.
goto p_confirm

:p_continue


echo ---- END ----
exit /b

:cancel
echo Program terminated ABRUPTLY.
exit /b