#!/usr/bin/env python3
"""
SecureShare Backend Startup Script
Run this to start the development server
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("🚀 Starting SecureShare Backend...")
    print("📁 Working directory:", backend_dir)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from template...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
        else:
            print("❌ .env.example not found")
    
    # Install dependencies if needed
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start server
    print("🌐 Starting server at http://localhost:8000")
    print("📚 API docs at http://localhost:8000/docs")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()