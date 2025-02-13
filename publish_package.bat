
@echo off
call .\activate.bat

call .\build.bat

echo Publising new release ...
python3 -m twine upload --repository testpypi dist/*