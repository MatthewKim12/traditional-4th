@echo off

echo Note: Running This File WITHOUT Python Will End Up With An Error
echo Go to https://www.python.org/downloads/ and download Python 3.13.9

py --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found!
    pause
    exit /b 1
)

py -m pip install pygame==2.6.1
pause