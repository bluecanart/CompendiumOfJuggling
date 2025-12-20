@echo off
REM Setup script for Trick Editor - Installs optional dependencies
REM Double-click this file to install Pillow for GIF preview support

echo ============================================
echo Trick Editor Setup
echo ============================================
echo.
echo This will install Pillow for GIF preview support.
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Installing Pillow...
python -m pip install --upgrade pip
python -m pip install Pillow

if errorlevel 1 (
    echo.
    echo Error installing Pillow!
    echo Make sure Python is installed and in your PATH.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo You can now run the Trick Editor with GIF preview support.
echo Double-click run_trick_editor.bat to start editing.
echo.
pause

