@echo off
call .\build_requirements.bat

git status
pause

git add .
git commit
git push --all