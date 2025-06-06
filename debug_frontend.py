#!/usr/bin/env python3
"""
Debug script to check frontend files and paths
"""

import os
import sys
from pathlib import Path


def check_frontend_files():
    """Check if frontend files exist and are properly built"""
    print("Frontend Debug Information")
    print("=" * 40)

    project_root = Path(__file__).parent
    frontend_dir = project_root / "frontend"
    dist_dir = frontend_dir / "dist"

    print(f"Project root: {project_root}")
    print(f"Frontend directory: {frontend_dir}")
    print(f"Dist directory: {dist_dir}")
    print()

    # Check if frontend directory exists
    if frontend_dir.exists():
        print("✓ Frontend directory exists")

        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if package_json.exists():
            print("✓ package.json exists")
        else:
            print("✗ package.json missing")

        # Check if dist directory exists
        if dist_dir.exists():
            print("✓ Dist directory exists")

            # List files in dist
            files = list(dist_dir.iterdir())
            print(f"Files in dist ({len(files)}):")
            for file in files:
                if file.is_file():
                    size = file.stat().st_size
                    print(f"  📄 {file.name} ({size:,} bytes)")
                elif file.is_dir():
                    subfiles = list(file.iterdir())
                    print(f"  📁 {file.name}/ ({len(subfiles)} items)")
                    for subfile in subfiles[:5]:  # Show first 5 items
                        if subfile.is_file():
                            size = subfile.stat().st_size
                            print(f"    📄 {subfile.name} ({size:,} bytes)")
                        else:
                            print(f"    📁 {subfile.name}/")
                    if len(subfiles) > 5:
                        print(f"    ... and {len(subfiles) - 5} more")

            # Check for index.html specifically
            index_html = dist_dir / "index.html"
            if index_html.exists():
                print("✓ index.html exists")
                size = index_html.stat().st_size
                print(f"  Size: {size:,} bytes")

                # Check content
                try:
                    with open(index_html, 'r', encoding='utf-8') as f:
                        content = f.read(500)  # First 500 chars
                        print(f"  Preview: {content[:100]}...")

                        # Check for common Vue.js indicators
                        if 'id="app"' in content:
                            print("  ✓ Contains Vue app mount point")
                        if 'script' in content:
                            print("  ✓ Contains script tags")
                        if 'link' in content:
                            print("  ✓ Contains link tags")

                except Exception as e:
                    print(f"  ✗ Could not read index.html: {e}")
            else:
                print("✗ index.html missing")

        else:
            print("✗ Dist directory does not exist")
            print("You need to build the frontend first:")
            print("  cd frontend")
            print("  npm install")
            print("  npm run build")

    else:
        print("✗ Frontend directory does not exist")

    print()
    print("Executable Bundle Check")
    print("=" * 25)

    # Check what would be bundled
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        print(f"Running as executable, bundle path: {base_path}")

        bundle_frontend = Path(base_path) / "frontend" / "dist"
        if bundle_frontend.exists():
            print("✓ Frontend files found in bundle")
            files = list(bundle_frontend.iterdir())
            print(f"Bundled files: {[f.name for f in files]}")
        else:
            print("✗ Frontend files not found in bundle")
            print(f"Expected at: {bundle_frontend}")
    else:
        print("Running as script (not bundled)")


def main():
    check_frontend_files()


if __name__ == "__main__":
    main()