#!/usr/bin/env python3
"""
Build script to create a single executable from FastAPI + Vue.js project
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def run_command(command, cwd=None, shell=False):
    """Run a command and handle errors"""
    print(f"Running: {command}")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, cwd=cwd, check=True,
                                    capture_output=True, text=True)
        else:
            result = subprocess.run(command, cwd=cwd, check=True,
                                    capture_output=True, text=True, shell=shell)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_dependencies():
    """Check if required tools are installed"""
    dependencies = ['node', 'npm', 'python']

    for dep in dependencies:
        try:
            result = subprocess.run([dep, '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ {dep} is not installed or not in PATH")
                return False
            print(f"✅ {dep} found: {result.stdout.strip()}")
        except FileNotFoundError:
            print(f"❌ {dep} is not installed or not in PATH")
            return False

    return True


def install_python_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")

    packages = [
        'pyinstaller',
        'fastapi',
        'uvicorn',
        'pydantic',
        # Add any other packages your FastAPI app needs
    ]

    for package in packages:
        if not run_command([sys.executable, '-m', 'pip', 'install', package]):
            return False

    return True


def build_vue_frontend():
    """Build the Vue.js frontend"""
    print("\n🔨 Building Vue.js frontend...")

    # Change to frontend directory (adjust path as needed)
    frontend_dir = Path('./frontend')  # Adjust this path to your Vue.js project
    if not frontend_dir.exists():
        frontend_dir = Path('./vue-frontend')  # Alternative path
    if not frontend_dir.exists():
        frontend_dir = Path('.')  # If Vue is in root directory

    # Install npm dependencies
    if not run_command('npm install', cwd=frontend_dir):
        return False

    # Build the project
    if not run_command('npm run build', cwd=frontend_dir):
        return False

    # Check if dist folder was created
    dist_path = frontend_dir / 'dist'
    if not dist_path.exists():
        print("❌ Build failed - dist folder not found")
        return False

    print("✅ Vue.js build completed")
    return True


def create_main_py():
    """Create the main.py file that will be compiled"""

    main_py_content = '''
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add your FastAPI app imports here
# from your_fastapi_app import app

# Create FastAPI app (replace this with your actual app)
app = FastAPI(title="D&D Character Manager")

# Determine if running as compiled executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running as script
    BASE_DIR = Path(__file__).parent

# Mount static files (Vue.js build)
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.get("/")
    async def serve_spa():
        return FileResponse(static_dir / "index.html")

    @app.get("/{path:path}")
    async def serve_spa_paths(path: str):
        file_path = static_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(static_dir / "index.html")

# Add your API routes here
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Example API route - replace with your actual routes
@app.get("/api/characters")
async def get_characters():
    return {"characters": {}, "campaign": {}}

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open("http://localhost:8998")

def main():
    """Main function to start the server"""
    print("🚀 Starting D&D Character Manager...")
    print("📊 Server will be available at: http://localhost:8998")

    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Start the server
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8998, 
        log_level="info",
        access_log=False
    )

if __name__ == "__main__":
    main()
'''

    with open('main.py', 'w') as f:
        f.write(main_py_content)

    print("✅ Created main.py")
    return True


def create_spec_file():
    """Create PyInstaller spec file for better control"""

    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('static', 'static')],  # Include Vue.js build files
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='DnDCharacterManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Add an icon file if you have one
)
'''

    with open('app.spec', 'w') as f:
        f.write(spec_content)

    print("✅ Created PyInstaller spec file")
    return True


def prepare_static_files():
    """Copy Vue.js build files to static directory"""
    print("\n📁 Preparing static files...")

    # Find the Vue build directory
    possible_paths = [
        Path('./frontend/dist'),
        Path('./vue-frontend/dist'),
        Path('./dist')
    ]

    dist_path = None
    for path in possible_paths:
        if path.exists():
            dist_path = path
            break

    if not dist_path:
        print("❌ Could not find Vue.js dist directory")
        return False

    # Create static directory
    static_dir = Path('./static')
    if static_dir.exists():
        shutil.rmtree(static_dir)

    # Copy dist contents to static
    shutil.copytree(dist_path, static_dir)
    print(f"✅ Copied {dist_path} to static/")

    return True


def build_executable():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building executable...")

    # Use spec file for better control
    command = [sys.executable, '-m', 'PyInstaller', '--clean', 'app.spec']

    if not run_command(command):
        print("❌ PyInstaller build failed")
        return False

    # Check if executable was created
    system = platform.system().lower()
    if system == "windows":
        exe_path = Path('./dist/DnDCharacterManager.exe')
    else:
        exe_path = Path('./dist/DnDCharacterManager')

    if exe_path.exists():
        print(f"✅ Executable created: {exe_path}")
        return True
    else:
        print("❌ Executable not found after build")
        return False


def cleanup():
    """Clean up build artifacts"""
    print("\n🧹 Cleaning up...")

    cleanup_paths = [
        'build',
        '__pycache__',
        'static',
        'main.py',
        'app.spec'
    ]

    for path in cleanup_paths:
        path_obj = Path(path)
        if path_obj.exists():
            if path_obj.is_dir():
                shutil.rmtree(path_obj)
            else:
                path_obj.unlink()
            print(f"🗑️ Removed {path}")


def main():
    """Main build process"""
    print("🏗️ D&D Character Manager Build Script")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies and try again")
        sys.exit(1)

    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)

    # Build Vue.js frontend
    if not build_vue_frontend():
        print("❌ Failed to build Vue.js frontend")
        sys.exit(1)

    # Prepare files for packaging
    if not prepare_static_files():
        print("❌ Failed to prepare static files")
        sys.exit(1)

    if not create_main_py():
        print("❌ Failed to create main.py")
        sys.exit(1)

    if not create_spec_file():
        print("❌ Failed to create spec file")
        sys.exit(1)

    # Build executable
    if not build_executable():
        print("❌ Failed to build executable")
        sys.exit(1)

    print("\n🎉 Build completed successfully!")
    print("📦 Your executable is in the 'dist' folder")

    # Ask if user wants to clean up
    response = input("\n🧹 Clean up build files? (y/N): ")
    if response.lower() in ['y', 'yes']:
        cleanup()

    print("\n✅ Done! You can now share the executable from the 'dist' folder.")


if __name__ == "__main__":
    main()