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
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from typing import Optional, List
from http import HTTPStatus

# Import our modules with fallback options
try:
    # First try package import
    from server.beyond_dnd import BeyondDnDClient, BeyondDnDAPIError

    logger.info("Imported server modules as package")
except ImportError:
    try:
        # Fallback to direct import
        from beyond_dnd import BeyondDnDClient, BeyondDnDAPIError

        logger.info("Imported server modules directly")
    except ImportError as e:
        logger.error(f"Failed to import server modules: {e}")
        sys.exit(1)

# Create FastAPI app here instead of importing
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize client
beyond = BeyondDnDClient()


# API Routes
@app.get('/characters')
def get_all_character_data(
        request: Request, char_ids: Optional[List[str]] = Query(None, nullable=True), force_update: bool = False
):
    try:
        char_data = beyond.get_all_characters_data(char_ids=char_ids, force_update=force_update)
    except BeyondDnDAPIError as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return JSONResponse(content=char_data)


@app.get("/characters/{char_id}")
def get_character_data(request: Request, char_id: str, force_update: bool = False):
    try:
        char_data = beyond.get_one_characters_data(char_id=char_id, force_update=force_update)
        return JSONResponse(content=char_data)
    except BeyondDnDAPIError as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.delete("/characters")
def delete_cached_data():
    try:
        beyond.delete_all_cached_character_data()
        return Response(status_code=HTTPStatus.ACCEPTED)
    except Exception as e:
        return JSONResponse(
            content={'message': f'An error occurred: {repr(e)}', 'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


class DnDSpellTracker:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8998
        self.frontend_url = f"http://{self.host}:{self.port}"

    def get_static_files_path(self):
        """Get the path to the built frontend files"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
            logger.info(f"Running as executable, base path: {base_path}")
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
            logger.info(f"Running as script, base path: {base_path}")

        static_path = os.path.join(base_path, 'frontend', 'dist')
        logger.info(f"Looking for frontend files at: {static_path}")

        # List contents to debug
        if os.path.exists(static_path):
            files = os.listdir(static_path)
            logger.info(f"Found files in dist: {files}")
        else:
            logger.warning(f"Static path does not exist: {static_path}")
            # Try alternative paths
            alt_paths = [
                os.path.join(base_path, 'dist'),
                os.path.join(base_path, 'frontend'),
                os.path.join(os.path.dirname(base_path), 'frontend', 'dist')
            ]
            for alt_path in alt_paths:
                logger.info(f"Trying alternative path: {alt_path}")
                if os.path.exists(alt_path):
                    logger.info(f"Alternative path exists: {alt_path}")
                    if os.path.isdir(alt_path):
                        files = os.listdir(alt_path)
                        logger.info(f"Files in {alt_path}: {files}")

        return static_path

    def get_static_files_path(self):
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
                    # List contents for debugging
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

    def setup_static_serving(self):
        """Setup static file serving for the frontend"""
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        from fastapi import HTTPException

        static_path = self.get_static_files_path()
        index_file = os.path.join(static_path, "index.html")
        assets_path = os.path.join(static_path, "assets")

        logger.info(f"Static path: {static_path}")
        logger.info(f"Index file: {index_file}")
        logger.info(f"Assets path: {assets_path}")
        logger.info(f"Index exists: {os.path.exists(index_file)}")
        logger.info(f"Assets exists: {os.path.exists(assets_path)}")

        # Mount assets FIRST - this should take precedence
        if os.path.exists(assets_path):
            try:
                app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
                logger.info("✓ Mounted /assets")
            except Exception as e:
                logger.warning(f"Could not mount assets: {e}")
        else:
            logger.warning(f"Assets directory not found: {assets_path}")

        # Serve favicon if it exists
        favicon_path = os.path.join(static_path, "favicon.ico")
        if os.path.exists(favicon_path):
            @app.get("/favicon.ico")
            async def serve_favicon():
                return FileResponse(favicon_path)

            logger.info("✓ Configured favicon route")

        # Add debug endpoint
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
                "frozen": getattr(sys, 'frozen', False)
            }

        # Root route
        @app.get("/")
        async def serve_index():
            logger.info(f"Root route requested, serving: {index_file}")
            if os.path.exists(index_file):
                return FileResponse(index_file, media_type="text/html")
            else:
                logger.error(f"index.html not found at: {index_file}")
                return {
                    "error": "Frontend index.html not found",
                    "path": index_file,
                    "static_path": static_path,
                    "exists": os.path.exists(static_path),
                    "files": os.listdir(static_path) if os.path.exists(static_path) else []
                }

        # Only create SPA route if index.html exists
        if os.path.exists(index_file):
            logger.info(f"✓ Frontend configured successfully")

            # SPA route handler - be very specific about what we catch
            @app.get("/{full_path:path}")
            async def serve_spa_routes(full_path: str = ""):
                # Explicitly exclude paths that should NOT be SPA routes
                excluded_prefixes = [
                    "api/", "characters/", "docs/", "redoc/", "openapi.json",
                    "assets/", "favicon.ico", "debug/", ".well-known/"
                ]

                # Exclude file extensions
                excluded_extensions = [
                    ".js", ".css", ".map", ".png", ".jpg", ".jpeg", ".gif",
                    ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".json"
                ]

                # If it's an excluded path or has an excluded extension, return 404
                if (any(full_path.startswith(prefix) for prefix in excluded_prefixes) or
                        any(full_path.endswith(ext) for ext in excluded_extensions)):
                    logger.info(f"Excluded path, returning 404: {full_path}")
                    raise HTTPException(status_code=404, detail="Not found")

                # For everything else (SPA routes), serve index.html
                logger.info(f"SPA route requested: '{full_path}', serving index.html")
                return FileResponse(index_file, media_type="text/html")

        else:
            logger.error(f"✗ Frontend setup failed - index.html not found")

    def open_browser(self):
        """Open the default web browser to the application"""
        time.sleep(3)  # Wait a bit longer for server to fully start
        try:
            logger.info(f"Opening browser to {self.frontend_url}")
            webbrowser.open(self.frontend_url)
            logger.info("✓ Browser opened")
        except Exception as e:
            logger.error(f"Could not open browser: {e}")
            logger.info(f"Please manually open: {self.frontend_url}")

    def run_server(self):
        """Run the FastAPI server"""
        try:
            logger.info(f"Starting server on {self.host}:{self.port}")
            uvicorn.run(
                app,
                host=self.host,
                port=self.port,
                log_level="info",
                access_log=True  # Enable access logs to see requests
            )
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            sys.exit(1)

    def start(self):
        """Start the application"""
        logger.info("=" * 50)
        logger.info("Starting DnD Spell Component Tracker...")
        logger.info(f"Server will run on {self.frontend_url}")
        logger.info("=" * 50)

        # Setup static file serving
        self.setup_static_serving()

        # Start browser in a separate thread
        browser_thread = threading.Thread(target=self.open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Start the server (this will block)
        self.run_server()


def main():
    """Main entry point"""
    try:
        tracker = DnDSpellTracker()
        tracker.start()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()