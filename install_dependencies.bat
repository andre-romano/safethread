@echo off
call .\activate.bat

echo "Upgrading pip ..."
python.exe -m pip install --upgrade pip setuptools wheel

echo "Installing setuptools, wheel, build, twine ..."
pip install setuptools wheel build twine

echo "Installing dependencies from requirements.txt ..."
pip install -r requirements.txt 
