@echo off
call .\activate.bat

echo build.bat - Begin

echo Cleaning build artifacts...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q *.egg-info
rmdir /s /q __pycache__
rmdir /s /q .pytest_cache
rmdir /s /q .mypy_cache

echo Building the package...
python -m build

echo Testing package...
twine check dist/*

echo build.bat - End