@echo off

git status

:confirm
echo " "
set /p "CONFIRM=Commit changes? (y/n): "
if /i "%CONFIRM%"=="y" goto continue
if /i "%CONFIRM%"=="n" goto cancel
echo Invalid option. Please, answer with y or n.
goto confirm

:continue
git add .
git commit
git push --all

echo " "
echo " "
echo ---- END ----
echo " "
echo " "
git status
exit /b

:cancel
echo Program terminated ABRUPTLY.
exit /b