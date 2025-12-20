@echo off
REM Launcher for the Juggling Trick Editor
REM Double-click this file to start the editor

cd /d "%~dp0"
python trick_editor.py

if errorlevel 1 (
    echo.
    echo Error running the trick editor!
    echo Make sure Python is installed and in your PATH.
    echo.
    pause
)

