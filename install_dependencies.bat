@echo off
call .\activate.bat
call .\build_requirements.bat

echo "Installing dependencies from requirements.txt ..."
pip3 install -r requirements.txt 
