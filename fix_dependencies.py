#!/usr/bin/env python3
"""
Quick fix script for dependency conflicts
"""

import subprocess
import sys

def run_command(command):
    """Run command and print output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def main():
    print("🔧 Fixing dependency conflicts...")
    print("=" * 40)
    
    # Uninstall conflicting packages
    print("1. Removing conflicting packages...")
    run_command("pip uninstall -y openai pyautogen autogen")
    
    # Install correct versions
    print("\n2. Installing compatible versions...")
    success = True
    
    packages = [
        "pyautogen==0.10.0",
        "autogen-agentchat==0.7.1",
        "autogen-ext[openai]==0.7.1",
        "openai==1.58.1",
        "streamlit==1.41.1"
    ]
    
    for package in packages:
        print(f"\nInstalling {package}...")
        if not run_command(f"pip install {package}"):
            success = False
            print(f"❌ Failed to install {package}")
    
    if success:
        print("\n✅ Dependencies fixed successfully!")
        print("You can now run: python run.py")
    else:
        print("\n❌ Some installations failed. Please check the errors above.")

if __name__ == "__main__":
    main()