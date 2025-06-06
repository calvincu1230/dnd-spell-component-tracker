#!/usr/bin/env python3
"""
Build script to create a single executable for the DnD Spell Component Tracker
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path


class ExecutableBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"
        self.server_dir = self.project_root / "server"
        self.dist_dir = self.project_root / "dist"

    def check_requirements(self):
        """Check if all required tools are installed"""
        print("Checking requirements...")

        # Check Node.js and npm
        try:
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            print("✓ Node.js and npm found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Node.js and npm are required. Please install them first.")
            return False

        # Check PyInstaller
        try:
            import PyInstaller
            print("✓ PyInstaller found")
        except ImportError:
            print("✗ PyInstaller not found. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
                print("✓ PyInstaller installed")
            except subprocess.CalledProcessError:
                print("✗ Failed to install PyInstaller")
                return False

        return True

    def build_frontend(self):
        """Build the Vue.js frontend"""
        print("\nBuilding frontend...")

        if not self.frontend_dir.exists():
            print("✗ Frontend directory not found")
            return False

        # Change to frontend directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.frontend_dir)

            # Install dependencies
            print("Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)

            # Build the frontend
            print("Building frontend...")
            subprocess.run(["npm", "run", "build"], check=True)

            print("✓ Frontend built successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"✗ Frontend build failed: {e}")
            return False
        finally:
            os.chdir(original_cwd)

    def install_backend_dependencies(self):
        """Install backend dependencies"""
        print("\nInstalling backend dependencies...")

        # Install specific versions to ensure compatibility
        dependencies = [
            "requests==2.32.3",
            "uvicorn==0.34.3",
            "aiohttp==3.12.4",
            "fastapi==0.115.12",
            "python-multipart==0.0.6",
            "pyinstaller>=5.0.0"
        ]

        for dep in dependencies:
            try:
                print(f"Installing {dep}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {dep}: {e}")
                return False

        print("✓ Backend dependencies installed")
        return True

    def create_spec_file(self):
        """Create PyInstaller spec file"""
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT

block_cipher = None

# Get the project root directory
project_root = os.path.dirname(os.path.abspath(SPEC))

# Add server directory to path for imports
sys.path.insert(0, os.path.join(project_root, 'server'))

a = Analysis(
    ['main.py'],
    pathex=[
        project_root,
        os.path.join(project_root, 'server')
    ],
    binaries=[],
    datas=[
        (os.path.join(project_root, 'frontend', 'dist'), 'frontend/dist'),
        (os.path.join(project_root, 'frontend', 'dist', 'index.html'), '.'),
        (os.path.join(project_root, 'frontend', 'dist', 'assets'), 'assets'),
    ],
    hiddenimports=[
        # Core dependencies
        'requests',
        'requests.adapters',
        'requests.auth',
        'requests.cookies',
        'requests.exceptions',
        'requests.models',
        'requests.packages',
        'requests.sessions',
        'requests.structures',
        'requests.utils',
        'urllib3',
        'urllib3.poolmanager',
        'urllib3.connectionpool',
        'charset_normalizer',
        'certifi',
        'idna',

        # FastAPI and Uvicorn
        'fastapi',
        'fastapi.staticfiles',
        'fastapi.responses',
        'fastapi.requests',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'starlette',
        'starlette.applications',
        'starlette.routing',
        'starlette.responses',
        'starlette.staticfiles',
        'starlette.middleware',
        'starlette.middleware.cors',
        'uvicorn',
        'uvicorn.main',
        'uvicorn.server',
        'uvicorn.config',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.websockets_impl',
        'uvicorn.protocols.http.httptools_impl',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.utils',
        'uvicorn.importer',
        'uvicorn.supervisors',
        'uvicorn.supervisors.basereload',
        'uvicorn.supervisors.statreload',
        'uvicorn.supervisors.watchfilesreload',
        'uvicorn.supervisors.watchgodreload',

        # HTTP libraries
        'h11',
        'httptools',
        'websockets',
        'websockets.legacy',
        'websockets.legacy.server',
        'websockets.legacy.client',

        # Async libraries
        'anyio',
        'sniffio',

        # Multipart
        'multipart',
        'multipart.multipart',
        'python_multipart',

        # JSON handling
        'json',
        'orjson',

        # Server modules
        'server',
        'server.beyond_dnd',
        'server.server',

        # Standard library modules that might be missed
        'threading',
        'webbrowser',
        'logging',
        'pathlib',
        'contextlib',
        'typing',
        'http',
        'http.client',
        'email',
        'email.message',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DnDSpellTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disabled UPX as it can cause issues on macOS
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Enable console for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file path here
)
'''

        spec_file = self.project_root / "dnd_spell_tracker.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)

        print("✓ Spec file created")
        return spec_file

    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("\nBuilding executable...")

        spec_file = self.create_spec_file()

        try:
            # Clean previous builds
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)

            build_dir = self.project_root / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)

            # Build the executable with verbose output for debugging
            cmd = [
                "pyinstaller",
                "--clean",
                "--log-level=INFO",
                str(spec_file)
            ]

            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            # Print any warnings from PyInstaller
            if result.stderr:
                print("PyInstaller warnings/info:")
                print(result.stderr)

            print("✓ Executable built successfully")

            # Find the executable
            if sys.platform == "win32":
                exe_name = "DnDSpellTracker.exe"
            else:
                exe_name = "DnDSpellTracker"

            exe_path = self.dist_dir / exe_name
            if exe_path.exists():
                print(f"✓ Executable created: {exe_path}")
                print(f"✓ File size: {exe_path.stat().st_size / (1024 * 1024):.1f} MB")

                # Make executable on Unix systems
                if sys.platform != "win32":
                    os.chmod(exe_path, 0o755)
                    print("✓ Set executable permissions")

                return True
            else:
                print("✗ Executable not found after build")
                return False

        except subprocess.CalledProcessError as e:
            print(f"✗ Executable build failed: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                print("Error details:")
                print(e.stderr)
            return False

    def create_distribution_package(self):
        """Create a distribution package with the executable and instructions"""
        print("\nCreating distribution package...")

        package_dir = self.project_root / "DnDSpellTracker"
        if package_dir.exists():
            shutil.rmtree(package_dir)

        package_dir.mkdir()

        # Copy executable
        if sys.platform == "win32":
            exe_name = "DnDSpellTracker.exe"
        else:
            exe_name = "DnDSpellTracker"

        exe_source = self.dist_dir / exe_name
        exe_dest = package_dir / exe_name

        if exe_source.exists():
            shutil.copy2(exe_source, exe_dest)

            # Create README
            readme_content = f"""# DnD Spell Component Tracker

## How to Use

1. Double-click on `{exe_name}` to start the application
2. The application will automatically open in your default web browser
3. Enter your D&D Beyond character IDs to load character data
4. View spells and their components, inventory, and focus items

## Features

- Track spell components and whether they're consumed or have costs
- View character inventory and custom spell material components
- Check if a focus can replace spell components
- Supports multiple characters from the same campaign

## Requirements

- No additional software needed! This is a portable executable.
- Internet connection required to fetch data from D&D Beyond
- Character profiles must be set to Public on D&D Beyond

## Troubleshooting

- If the browser doesn't open automatically, manually navigate to: http://127.0.0.1:8998
- Make sure your character profiles are set to Public on D&D Beyond
- If you encounter firewall warnings, allow the application to communicate

## Character ID Setup

1. Go to your D&D Beyond character sheet
2. Look at the URL: https://www.dndbeyond.com/characters/12345678
3. The number at the end (12345678) is your character ID
4. Enter this ID in the application

Enjoy tracking your spell components!
"""

            readme_file = package_dir / "README.txt"
            with open(readme_file, 'w') as f:
                f.write(readme_content)

            print(f"✓ Distribution package created: {package_dir}")
            return True

        return False

    def build_all(self):
        """Run the complete build process"""
        print("DnD Spell Component Tracker - Build Process")
        print("=" * 50)

        if not self.check_requirements():
            return False

        if not self.build_frontend():
            return False

        if not self.install_backend_dependencies():
            return False

        if not self.build_executable():
            return False

        if not self.create_distribution_package():
            return False

        print("\n" + "=" * 50)
        print("✓ Build completed successfully!")
        print("✓ Your executable is ready for distribution")
        print(f"✓ Distribution package: {self.project_root / 'DnDSpellTracker'}")

        return True


def main():
    builder = ExecutableBuilder()
    success = builder.build_all()

    if not success:
        print("\n✗ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()