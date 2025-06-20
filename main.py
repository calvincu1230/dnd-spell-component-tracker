#!/usr/bin/env python3
"""
DnD Spell Component Tracker - Single Executable
Main entry point that serves both the FastAPI backend and Vue.js frontend
"""

import os
import sys
import threading
import time
import webbrowser
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the server directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(current_dir, 'server')
sys.path.insert(0, server_dir)

# Import all dependencies explicitly to help PyInstaller
import requests
import uvicorn
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException

# Import the existing FastAPI app
try:
    from server.server import app
    logger.info("Imported FastAPI app from server package")
except ImportError:
    try:
        import server as server_module
        app = server_module.app
        logger.info("Imported FastAPI app directly")
    except ImportError as e:
        logger.error(f"Failed to import server app: {e}")
        sys.exit(1)


def get_static_files_path():
    """Get the path to the built frontend files"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
        logger.info(f"Running as executable, base path: {base_path}")
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Running as script, base path: {base_path}")

    # Try multiple possible paths for the frontend files
    possible_paths = [
        os.path.join(base_path, 'frontend', 'dist'),
        os.path.join(base_path, 'dist'),
        os.path.join(base_path, '..', 'frontend', 'dist'),
        os.path.join(os.path.dirname(base_path), 'frontend', 'dist')
    ]

    for static_path in possible_paths:
        logger.info(f"Checking path: {static_path}")
        if os.path.exists(static_path):
            index_file = os.path.join(static_path, 'index.html')
            if os.path.exists(index_file):
                logger.info(f"✓ Found frontend files at: {static_path}")
                try:
                    files = os.listdir(static_path)
                    logger.info(f"Frontend files: {files}")
                except:
                    pass
                return static_path
            else:
                logger.info(f"Path exists but no index.html: {static_path}")
        else:
            logger.info(f"Path does not exist: {static_path}")

    # If no path worked, return the default and log the issue
    default_path = os.path.join(base_path, 'frontend', 'dist')
    logger.error(f"No valid frontend path found, using default: {default_path}")
    return default_path


def setup_frontend_serving():
    """Setup static file serving for the frontend"""
    static_path = get_static_files_path()
    index_file = os.path.join(static_path, "index.html")
    assets_path = os.path.join(static_path, "assets")

    logger.info(f"Static path: {static_path}")
    logger.info(f"Index file: {index_file}")
    logger.info(f"Assets path: {assets_path}")
    logger.info(f"Index exists: {os.path.exists(index_file)}")
    logger.info(f"Assets exists: {os.path.exists(assets_path)}")

    # Check if routes are already defined (to avoid duplicates)
    existing_routes = [route.path for route in app.routes]
    logger.info(f"Existing routes: {existing_routes}")

    # Mount static files BEFORE any route definitions
    if os.path.exists(assets_path) and "/assets" not in [str(route.path) for route in app.routes if hasattr(route, 'path')]:
        try:
            app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
            logger.info("✓ Mounted /assets")
        except Exception as e:
            logger.warning(f"Could not mount assets: {e}")

    # Mount the entire static directory as well for direct file access
    if os.path.exists(static_path) and "/static" not in [str(route.path) for route in app.routes if hasattr(route, 'path')]:
        try:
            app.mount("/static", StaticFiles(directory=static_path), name="static")
            logger.info("✓ Mounted /static")
        except Exception as e:
            logger.warning(f"Could not mount static: {e}")

    # Only add frontend routes if we don't already have them and if frontend exists
    if os.path.exists(index_file):
        # Serve favicon
        favicon_path = os.path.join(static_path, "favicon.ico")
        if os.path.exists(favicon_path) and "/favicon.ico" not in existing_routes:
            @app.get("/favicon.ico")
            async def serve_favicon():
                return FileResponse(favicon_path)
            logger.info("✓ Configured favicon route")

        # Add debug endpoint if it doesn't exist
        if "/debug" not in existing_routes:
            @app.get("/debug")
            async def debug_info():
                return {
                    "static_path": static_path,
                    "index_file": index_file,
                    "index_exists": os.path.exists(index_file),
                    "static_exists": os.path.exists(static_path),
                    "files": os.listdir(static_path) if os.path.exists(static_path) else [],
                    "assets_files": os.listdir(assets_path) if os.path.exists(assets_path) else [],
                    "base_path": sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(
                        os.path.abspath(__file__)),
                    "frozen": getattr(sys, 'frozen', False),
                    "routes": [route.path for route in app.routes]
                }
            logger.info("✓ Configured debug route")

        # Root route - serve index.html (only if it doesn't exist)
        if "/" not in existing_routes:
            @app.get("/")
            async def serve_index():
                logger.info(f"Root route requested, serving: {index_file}")
                return FileResponse(index_file, media_type="text/html")
            logger.info("✓ Configured root route")

        # SPA catch-all route - ONLY if we have a valid frontend and no catch-all exists
        catch_all_exists = any(
            "path:path" in str(route.path_regex) for route in app.routes if hasattr(route, 'path_regex'))
        if not catch_all_exists:
            @app.get("/{full_path:path}")
            async def serve_spa_routes(full_path: str = ""):
                # Exclude API and static file routes
                excluded_prefixes = [
                    "api", "characters", "docs", "redoc", "openapi.json",
                    "assets", "static", "favicon.ico", "debug", ".well-known"
                ]

                # Exclude file extensions that should return 404
                excluded_extensions = [
                    ".js", ".css", ".map", ".png", ".jpg", ".jpeg", ".gif",
                    ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".json", ".txt"
                ]

                # Check if this should be excluded
                if (any(full_path.startswith(prefix) for prefix in excluded_prefixes) or
                        any(full_path.endswith(ext) for ext in excluded_extensions)):
                    logger.info(f"Excluded path: {full_path}")
                    raise HTTPException(status_code=404, detail="Not found")

                # Serve index.html for SPA routes
                logger.info(f"SPA route: {full_path}")
                return FileResponse(index_file, media_type="text/html")
            logger.info("✓ Configured SPA catch-all route")
        else:
            logger.info("Catch-all route already exists, skipping")
    else:
        logger.error("✗ Frontend not available - no frontend routes configured")


def open_browser():
    """Open the default web browser to the application"""
    time.sleep(3)  # Wait for server to fully start
    try:
        frontend_url = "http://127.0.0.1:8998"
        logger.info(f"Opening browser to {frontend_url}")
        webbrowser.open(frontend_url)
        logger.info("✓ Browser opened")
    except Exception as e:
        logger.error(f"Could not open browser: {e}")
        logger.info("Please manually open: http://127.0.0.1:8998")


def main():
    """Main entry point"""
    try:
        logger.info("=" * 50)
        logger.info("Starting DnD Spell Component Tracker...")
        logger.info("Server will run on http://127.0.0.1:8998")
        logger.info("=" * 50)

        # Setup frontend serving
        setup_frontend_serving()

        # Start browser in a separate thread
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Start the server
        logger.info("Starting server on 127.0.0.1:8998")
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8998,
            log_level="info",
            access_log=True,
            reload=False  # Important: Disable auto-reload to prevent restart issues
        )

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()