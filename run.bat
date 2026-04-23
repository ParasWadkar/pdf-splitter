@echo off
REM PDF Splitter - Batch File Launcher
REM Simply double-click this file to start the GUI

cd /d "%~dp0"

REM Activate virtual environment and run the GUI
call .venv\Scripts\activate.bat
python gui.py

pause
