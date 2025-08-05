#!/usr/bin/env python3
"""
Simple startup script for running FastAPI backend and Streamlit UI
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please create a .env file with your OpenAI API key")
        return False
    print("✅ Environment configured")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "output"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created necessary directories")

def start_fastapi():
    """Start FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ])

def start_streamlit():
    """Start Streamlit UI"""
    print("🎨 Starting Streamlit UI...")
    return subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", 
        "streamlit_ui.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

def main():
    """Main function to start both services"""
    print("📋 Requirements Analyzer - UI Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        return
    
    # Create directories
    create_directories()
    
    print("\n🚀 Starting services...")
    print("=" * 40)
    
    # Start FastAPI backend
    fastapi_process = start_fastapi()
    
    # Wait for FastAPI to start
    print("⏳ Waiting for FastAPI to start...")
    time.sleep(3)
    
    # Start Streamlit UI
    streamlit_process = start_streamlit()
    
    print("\n✅ Both services started!")
    print("=" * 40)
    print("🔗 FastAPI Backend: http://localhost:8000")
    print("📋 API Docs: http://localhost:8000/docs")
    print("🎨 Streamlit UI: http://localhost:8501")
    print("=" * 40)
    print("\n💡 How to use:")
    print("1. Open http://localhost:8501 in your browser")
    print("2. Upload a requirements document")
    print("3. Review the generated SRDs")
    print("4. Accept or reject each SRD")
    print("\n⚠️  Press Ctrl+C to stop both services")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if fastapi_process.poll() is not None:
                print("❌ FastAPI died, restarting...")
                fastapi_process = start_fastapi()
            
            if streamlit_process.poll() is not None:
                print("❌ Streamlit died, restarting...")
                streamlit_process = start_streamlit()
    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        
        fastapi_process.terminate()
        streamlit_process.terminate()
        
        time.sleep(2)
        
        try:
            fastapi_process.kill()
            streamlit_process.kill()
        except:
            pass
        
        print("✅ Services stopped")

if __name__ == "__main__":
    main()