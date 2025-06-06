# build.bat (for Windows)
@echo off
echo Building DnD Spell Component Tracker...

REM Install PyInstaller if not present
python -m pip install pyinstaller

REM Run the build script
python build_executable.py

echo Build complete!
pause
