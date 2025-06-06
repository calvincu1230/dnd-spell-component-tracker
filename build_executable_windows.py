#!/usr/bin/env python3
"""
Windows-specific build script for the DnD Spell Component Tracker
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path


class WindowsExecutableBuilder:
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
            result = subprocess.run(["node", "--version"], check=True, capture_output=True, text=True, shell=True)
            print(f"✓ Node.js found: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Node.js is required. Please install it first.")
            return False
        
        try:
            result = subprocess.run(["npm", "--version"], check=True, capture_output=True, text=True, shell=True)
            print(f"✓ npm found: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ npm is required. Please install it first.")
            return False
        
        # Check Python version
        print(f"✓ Python version: {sys.version}")
        
        # Check PyInstaller
        try:
            import PyInstaller
            print(f"✓ PyInstaller found: {PyInstaller.__version__}")
        except ImportError:
            print("✗ PyInstaller not found. It will be installed with other dependencies.")
        
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
            result = subprocess.run(["npm", "install"], check=True, capture_output=True, text=True, shell=True)
            if result.stderr:
                print(f"npm install warnings: {result.stderr}")
            
            # Build the frontend
            print("Building frontend...")
            result = subprocess.run(["npm", "run", "build"], check=True, capture_output=True, text=True, shell=True)
            if result.stderr:
                print(f"npm build warnings: {result.stderr}")
            
            print("✓ Frontend built successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Frontend build failed: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Error details: {e.stderr}")
            if hasattr(e, 'stdout') and e.stdout:
                print(f"Output: {e.stdout}")
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
            "python-multipart==0.0.6"
        ]
        
        # Check PyInstaller separately since it's already installed
        try:
            import PyInstaller
            print(f"✓ PyInstaller already installed: {PyInstaller.__version__}")
        except ImportError:
            print("Installing PyInstaller...")
            dependencies.append("pyinstaller")
        
        for dep in dependencies:
            try:
                print(f"Installing {dep}...")
                # Split the dependency string properly for subprocess
                pip_cmd = [sys.executable, "-m", "pip", "install", dep]
                result = subprocess.run(
                    pip_cmd, 
                    check=True, 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
                # Print successful installation output quietly
                print(f"  ✓ {dep}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {dep}: {e}")
                if hasattr(e, 'stderr') and e.stderr:
                    print(f"Error details: {e.stderr}")
                if hasattr(e, 'stdout') and e.stdout:
                    print(f"Output: {e.stdout}")
                return False
        
        print("✓ Backend dependencies installed")
        return True
    
    def create_spec_file(self):
        """Create PyInstaller spec file optimized for Windows"""
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
        
        # Windows-specific
        'winreg',
        'msvcrt',
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
    upx=False,  # Disabled UPX for Windows compatibility
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
        
        spec_file = self.project_root / "dnd_spell_tracker_windows.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        print("✓ Windows spec file created")
        return spec_file
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("\nBuilding Windows executable...")
        
        spec_file = self.create_spec_file()
        
        try:
            # Clean previous builds
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
            
            build_dir = self.project_root / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)
            
            # Build the executable with Windows-specific options
            cmd = [
                "pyinstaller",
                "--clean",
                "--log-level=INFO",
                "--distpath", str(self.dist_dir),
                str(spec_file)
            ]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=True)
            
            # Print build info
            if result.stdout:
                print("PyInstaller output:")
                print(result.stdout)
            if result.stderr:
                print("PyInstaller warnings:")
                print(result.stderr)
            
            print("✓ Executable built successfully")
            
            # Find the executable
            exe_name = "DnDSpellTracker.exe"
            exe_path = self.dist_dir / exe_name
            
            if exe_path.exists():
                print(f"✓ Executable created: {exe_path}")
                print(f"✓ File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
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
        print("\nCreating Windows distribution package...")
        
        package_dir = self.project_root / "DnDSpellTracker_Windows"
        
        # Try to remove existing directory, but don't fail if we can't
        if package_dir.exists():
            try:
                # Try to remove read-only attributes first
                import stat
                for root, dirs, files in os.walk(package_dir):
                    for dir_name in dirs:
                        os.chmod(os.path.join(root, dir_name), stat.S_IWRITE)
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        os.chmod(file_path, stat.S_IWRITE)
                
                shutil.rmtree(package_dir)
                print("✓ Cleaned up existing package directory")
            except PermissionError as e:
                print(f"⚠ Could not remove existing directory: {e}")
                print("  Trying to create package anyway...")
                # Try with a different name
                import time
                timestamp = int(time.time())
                package_dir = self.project_root / f"DnDSpellTracker_Windows_{timestamp}"
                print(f"  Using alternative directory: {package_dir.name}")
        
        # Create the package directory
        try:
            package_dir.mkdir(exist_ok=True)
        except Exception as e:
            print(f"✗ Could not create package directory: {e}")
            return False
        
        # Copy executable
        exe_name = "DnDSpellTracker.exe"
        exe_source = self.dist_dir / exe_name
        exe_dest = package_dir / exe_name
        
        if exe_source.exists():
            try:
                shutil.copy2(exe_source, exe_dest)
                print(f"✓ Copied executable to: {exe_dest}")
            except Exception as e:
                print(f"✗ Could not copy executable: {e}")
                return False
            
            # Create README
            readme_content = f"""# DnD Spell Component Tracker - Windows

## How to Use

1. Double-click on `{exe_name}` to start the application
2. Windows may show a security warning - click "More info" then "Run anyway"
3. The application will automatically open in your default web browser
4. Enter your D&D Beyond character IDs to load character data
5. View spells and their components, inventory, and focus items

## Features

- Track spell components and whether they're consumed or have costs
- View character inventory and custom spell material components
- Check if a focus can replace spell components
- Supports multiple characters from the same campaign

## Windows Security Notice

Since this is an unsigned executable, Windows Defender may flag it as potentially unwanted software. This is normal for unsigned applications. You can:

1. Click "More info" and then "Run anyway" when the warning appears
2. Add an exception in Windows Defender if needed

## Requirements

- No additional software needed! This is a portable executable.
- Internet connection required to fetch data from D&D Beyond
- Character profiles must be set to Public on D&D Beyond

## Troubleshooting

- If Windows blocks the executable, right-click and select "Run as administrator"
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
            try:
                with open(readme_file, 'w') as f:
                    f.write(readme_content)
                print("✓ Created README.txt")
            except Exception as e:
                print(f"⚠ Could not create README: {e}")
            
            print(f"✓ Windows distribution package created: {package_dir}")
            return True
        else:
            print(f"✗ Executable not found at: {exe_source}")
            return False
    
    def build_all(self):
        """Run the complete build process"""
        print("DnD Spell Component Tracker - Windows Build Process")
        print("=" * 60)
        
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
        
        print("\n" + "=" * 60)
        print("✓ Windows build completed successfully!")
        print("✓ Your Windows executable is ready for distribution")
        print(f"✓ Distribution package: {self.project_root / 'DnDSpellTracker_Windows'}")
        
        return True

def main():
    builder = WindowsExecutableBuilder()
    success = builder.build_all()
    
    if not success:
        print("\n✗ Windows build failed!")
        input("Press Enter to exit...")
        sys.exit(1)
    else:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()