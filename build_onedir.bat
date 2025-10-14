@echo off
echo ========================================
echo Claude Monitor - Build ONEDIR version
echo ========================================
echo.

echo This builds a folder with all files instead of single exe.
echo This is more reliable for opencv-python.
echo.

echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Building ONEDIR version...
pyinstaller --name=ClaudeMonitor ^
  --onedir ^
  --windowed ^
  --collect-all=cv2 ^
  --collect-all=numpy ^
  --hidden-import=PIL ^
  --hidden-import=pyautogui ^
  --hidden-import=win32gui ^
  --hidden-import=win32con ^
  --noupx ^
  monitor_tool.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Files location: dist\ClaudeMonitor\
    echo Main executable: dist\ClaudeMonitor\ClaudeMonitor.exe
    echo.
    echo To run:
    echo   cd dist\ClaudeMonitor
    echo   ClaudeMonitor.exe
    echo.
    echo Note: The entire ClaudeMonitor folder must be kept together.
    echo.
) else (
    echo.
    echo Build failed! Check errors above.
)

pause
