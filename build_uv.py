#!/usr/bin/env python3
"""
Build and publish the mkdocstrings-twincat package using uv.
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a command and print its output."""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, check=True)
    return process.returncode

def build_package():
    """Build the package using uv."""
    print("Building package with uv...")
    run_command("uv build")
    print("Package built successfully.")

def publish_package():
    """Publish the package to PyPI using uv."""
    print("Publishing package to PyPI with uv...")
    run_command("uv publish dist/*")
    print("Package published successfully.")

def main():
    """Main function."""
    # Clean up previous builds
    if os.path.exists("dist"):
        print("Cleaning up previous builds...")
        try:
            import shutil
            shutil.rmtree("dist")
        except Exception as e:
            print(f"Error removing dist directory: {e}")
    
    # Build the package
    build_package()
    
    # Ask if the user wants to publish the package
    publish = input("Do you want to publish the package to PyPI? (y/n): ")
    if publish.lower() == "y":
        publish_package()
    else:
        print("Package not published.")
    
    print("Done.")

if __name__ == "__main__":
    main()
