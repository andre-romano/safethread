
@echo off
call .\activate.bat

echo "Upgrading pip ..."
python.exe -m pip install --upgrade pip setuptools wheel

echo "Installing pip-tools, setuptools, wheel ..."
pip install pip-tools setuptools wheel

echo "Creating requirements.txt ..."
pip-compile setup.py
