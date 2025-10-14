@echo off
echo ========================================
echo Claude Monitor Tool - Starting...
echo ========================================
echo.

REM Check if running from exe or python
if exist "ClaudeMonitor.exe" (
    echo Running from executable...
    ClaudeMonitor.exe
    if %errorlevel% neq 0 (
        echo.
        echo Error occurred! Error code: %errorlevel%
        pause
    )
) else if exist "dist\ClaudeMonitor.exe" (
    echo Running from executable in dist folder...
    cd dist
    ClaudeMonitor.exe
    cd ..
    if %errorlevel% neq 0 (
        echo.
        echo Error occurred! Error code: %errorlevel%
        pause
    )
) else (
    echo Running from Python...
    python --version
    if %errorlevel% neq 0 (
        echo Error: Python is not installed or not in PATH
        pause
        exit /b 1
    )
    echo.
    python monitor_tool.py
    if %errorlevel% neq 0 (
        echo.
        echo Error occurred! Error code: %errorlevel%
        pause
    )
)
