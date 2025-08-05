#!/usr/bin/env python3
"""
Setup script for Requirements Analyzer
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ is required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def uninstall_conflicting_packages():
    """Uninstall potentially conflicting packages"""
    conflicting_packages = ["openai", "pyautogen", "autogen", "autogen-agentchat", "autogen-ext"]
    
    for package in conflicting_packages:
        print(f"🗑️  Uninstalling {package} (if present)...")
        subprocess.run(f"pip uninstall -y {package}", shell=True, capture_output=True)

def install_requirements():
    """Install requirements with specific versions"""
    print("📦 Installing requirements...")
    
    # First, uninstall any existing versions to avoid conflicts
    uninstall_conflicting_packages()
    
    # Install specific versions
    packages = [
        "fastapi==0.116.1",
        "uvicorn[standard]==0.32.1",
        "python-multipart==0.0.18",
        "pyautogen==0.10.0",
        "autogen-agentchat==0.7.1",
        "autogen-ext[openai]==0.7.1",
        "openai==1.58.1",
        "python-dotenv==1.0.1",
        "pydantic==2.10.4",
        "aiofiles==24.1.0",
        "PyPDF2==3.1.0",
        "python-docx==1.1.2",
        "streamlit==1.41.1"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("OPENAI_MODEL=gpt-4\n")
        print("✅ .env file created. Please update it with your OpenAI API key.")
        return False
    else:
        print("✅ .env file already exists")
        return True

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "output", "test_output"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created necessary directories")

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("🔍 Verifying installation...")
    
    try:
        import autogen_agentchat
        import autogen_ext
        import openai
        import fastapi
        print("✅ All core packages imported successfully")
        
        # Check OpenAI API key
        from app.config import settings
        if settings.OPENAI_API_KEY == "" or "your_openai_api_key_here" in settings.OPENAI_API_KEY:
            print("⚠️  OpenAI API key not configured. Please update your .env file.")
            return False
        
        print("✅ Configuration verified")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Requirements Analyzer Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    env_created = create_env_file()
    
    # Verify installation
    if env_created and verify_installation():
        print("\n" + "=" * 50)
        print("🎉 Setup completed successfully!")
        print("To start the application, run: python run.py")
        print("API documentation will be available at: http://localhost:8000/docs")
    else:
        print("\n" + "=" * 50)
        print("⚠️  Setup completed with warnings.")
        print("Please update your .env file with a valid OpenAI API key before running the application.")

if __name__ == "__main__":
    main()