"""
Setup script to help initialize the project.
Run this to verify dependencies and create necessary directories.
"""
import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        "output",
        "models",
        "data/samples",
        "backend/app",
        "frontend/src/components",
        "frontend/src/utils",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created/verified directory: {directory}")

def check_python_version():
    """Check if Python version is 3.10+."""
    if sys.version_info < (3, 10):
        print("✗ Python 3.10+ is required")
        return False
    print(f"✓ Python version: {sys.version}")
    return True

def main():
    print("Setting up DEXA to 3D Avatar project...")
    print()
    
    if not check_python_version():
        sys.exit(1)
    
    create_directories()
    
    print()
    print("Setup complete!")
    print()
    print("Next steps:")
    print("1. Backend: cd backend && pip install -r requirements.txt")
    print("2. Frontend: cd frontend && npm install")
    print("3. Start backend: uvicorn app.main:app --reload")
    print("4. Start frontend: npm run dev")

if __name__ == "__main__":
    main()

