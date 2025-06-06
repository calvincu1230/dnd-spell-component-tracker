#!/bin/bash
# for Linux/macOS

echo "Building DnD Spell Component Tracker..."

# Install PyInstaller if not present
python3 -m pip install pyinstaller

# Run the build script
python3 build_executable.py

echo "Build complete!"