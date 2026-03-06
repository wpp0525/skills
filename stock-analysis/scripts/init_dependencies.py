#!/usr/bin/env python3
"""
Initialize and install dependencies for stock-analysis skill.

This script helps set up the skill environment when integrated with Claude Code.
It attempts to install all required dependencies using the most compatible method.
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install dependencies from requirements.txt"""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"Error: requirements.txt not found at {requirements_file}", file=sys.stderr)
        return False
    
    print(f"Installing dependencies from {requirements_file}...")
    
    # Try different installation methods
    install_methods = [
        {
            "name": "System-wide (with bypass)",
            "cmd": [sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", str(requirements_file)]
        },
        {
            "name": "User-level install",
            "cmd": [sys.executable, "-m", "pip", "install", "--user", "-r", str(requirements_file)]
        },
        {
            "name": "Standard install",
            "cmd": [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        },
    ]
    
    for method in install_methods:
        try:
            print(f"\nTrying: {method['name']}...", file=sys.stderr)
            result = subprocess.run(method["cmd"], timeout=180, check=False)
            if result.returncode == 0:
                print(f"✓ Successfully installed dependencies via: {method['name']}", file=sys.stderr)
                return True
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout during: {method['name']}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"✗ Error during {method['name']}: {e}", file=sys.stderr)
            continue
    
    return False


def check_dependencies():
    """Check if all required packages are available"""
    required_packages = {
        "AIShareTxt": "aishare-txt",
        "akshare": "akshare",
        "talib": "TA-Lib",
        "pandas": "pandas",
        "numpy": "numpy",
        "scipy": "scipy",
    }
    
    missing = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {import_name} is installed", file=sys.stderr)
        except ImportError:
            print(f"✗ {import_name} is NOT installed (package: {package_name})", file=sys.stderr)
            missing.append(package_name)
    
    return len(missing) == 0, missing


def main():
    """Main initialization routine"""
    print("Initializing stock-analysis skill dependencies...", file=sys.stderr)
    print("-" * 60, file=sys.stderr)
    
    # Check current status
    all_installed, missing = check_dependencies()
    
    if all_installed:
        print("\n✓ All dependencies are already installed!", file=sys.stderr)
        return 0
    
    print(f"\n✗ Missing packages: {', '.join(missing)}", file=sys.stderr)
    print("\nAttempting to install missing dependencies...", file=sys.stderr)
    print("-" * 60, file=sys.stderr)
    
    if install_dependencies():
        print("\n" + "=" * 60, file=sys.stderr)
        print("SUCCESS: Dependencies installed!", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        return 0
    else:
        print("\n" + "=" * 60, file=sys.stderr)
        print("FAILED: Could not install dependencies automatically.", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("\nManual fix options:", file=sys.stderr)
        print("1. Run: pip install --break-system-packages -r requirements.txt", file=sys.stderr)
        print("2. Run: pip install --user -r requirements.txt", file=sys.stderr)
        print("3. Install TA-Lib first: brew install ta-lib (macOS) or sudo apt-get install ta-lib (Linux)", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
