@echo off
echo ========================================
echo Claude Monitor Tool - Installation
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installation completed successfully!
    echo ========================================
    echo.
    echo You can now run the program using:
    echo   1. Double-click run.bat
    echo   2. Or run: python monitor_tool.py
    echo.
    echo To build exe file, run: build.bat
    echo ========================================
) else (
    echo.
    echo Installation failed. Please check the error messages above.
)

echo.
pause
