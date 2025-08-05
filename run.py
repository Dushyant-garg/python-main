#!/usr/bin/env python3
"""
Startup script for the Requirements Analyzer application
"""

import uvicorn
import os
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "output"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with the following content:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("OPENAI_MODEL=gpt-4")
        return False
    
    print("✓ Environment variables are properly configured")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Requirements Analyzer...")
    
    # Create necessary directories
    create_directories()
    
    # Check environment
    if not check_environment():
        print("\n❌ Startup failed. Please fix the environment configuration.")
        return
    
    print("\n✓ All checks passed!")
    print("🌐 Starting FastAPI server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("\n" + "="*50)
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()