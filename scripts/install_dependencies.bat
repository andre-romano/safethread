@echo off
call .\scripts\activate.bat

echo "Upgrading pip ..."
python.exe -m pip install --upgrade pip setuptools wheel

echo "Installing setuptools, wheel, build, twine, pytest-xdist, pydeps ..."
pip install setuptools wheel build twine pytest-xdist pydeps

echo "Installing dependencies from requirements.txt ..."
pip install -r requirements.txt 
