@echo off
call .\activate.bat

if exist .\requirements.lock (
    echo File requirements.lock found, installing dependencies...
    pip3 install -r .\requirements.lock --prefer-binary --no-cache-dir
) else if exist .\requirements.txt (
    echo Installing dependencies from requirements.txt ...
    pip3 install -r requirements.txt --prefer-binary --no-cache-dir
)

echo Freezing depedencies in requirements.lock ...
pip3 freeze > .\requirements.lock
