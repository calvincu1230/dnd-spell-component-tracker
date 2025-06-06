#!/usr/bin/env python3
"""
Test script to verify all dependencies are working before building
"""

import sys
import os

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))


def test_imports():
    """Test all critical imports"""
    print("Testing dependencies...")

    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False

    try:
        import uvicorn
        print("✓ uvicorn imported successfully")
    except ImportError as e:
        print(f"✗ uvicorn import failed: {e}")
        return False

    try:
        import fastapi
        print("✓ fastapi imported successfully")
    except ImportError as e:
        print(f"✗ fastapi import failed: {e}")
        return False

    try:
        from fastapi.staticfiles import StaticFiles
        print("✓ fastapi.staticfiles imported successfully")
    except ImportError as e:
        print(f"✗ fastapi.staticfiles import failed: {e}")
        return False

    try:
        # Try package import first
        try:
            from server.beyond_dnd import BeyondDnDClient, BeyondDnDAPIError
            print("✓ beyond_dnd module imported successfully (package import)")
        except ImportError:
            # Fallback to direct import
            import beyond_dnd
            from beyond_dnd import BeyondDnDClient, BeyondDnDAPIError
            print("✓ beyond_dnd module imported successfully (direct import)")
    except ImportError as e:
        print(f"✗ beyond_dnd import failed: {e}")
        return False

    try:
        # Try package import first
        try:
            from server.server import app
            print("✓ server module imported successfully (package import)")
        except ImportError:
            # Fallback to direct import
            import server as server_module
            app = server_module.app
            print("✓ server module imported successfully (direct import)")
    except ImportError as e:
        print(f"✗ server import failed: {e}")
        return False

    return True


def test_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")

    try:
        # Try package import first
        try:
            from server.beyond_dnd import BeyondDnDClient
            print("✓ BeyondDnDClient instantiated successfully (package import)")
        except ImportError:
            # Fallback to direct import
            from beyond_dnd import BeyondDnDClient
            print("✓ BeyondDnDClient instantiated successfully (direct import)")

        client = BeyondDnDClient()
    except Exception as e:
        print(f"✗ BeyondDnDClient instantiation failed: {e}")
        return False

    try:
        import requests
        # Test a simple request
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✓ HTTP requests working")
        else:
            print(f"✗ HTTP request failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ HTTP request test failed: {e}")
        return False

    return True


def main():
    print("Dependency Test Script")
    print("=" * 30)

    if not test_imports():
        print("\n✗ Import tests failed!")
        sys.exit(1)

    if not test_functionality():
        print("\n✗ Functionality tests failed!")
        sys.exit(1)

    print("\n✓ All tests passed! Ready to build executable.")


if __name__ == "__main__":
    main()