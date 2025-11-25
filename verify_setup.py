"""
Quick verification script to check if the project is set up correctly.
Run this before testing the full pipeline.
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required. Current:", sys.version)
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_backend_dependencies():
    """Check if backend dependencies are installed."""
    try:
        import fastapi
        import pdfplumber
        import trimesh
        import mediapipe
        import numpy
        print("✅ Backend dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e.name}")
        print("   Run: cd backend && pip install -r requirements.txt")
        return False

def check_backend_structure():
    """Check if backend files exist."""
    required_files = [
        "backend/app/main.py",
        "backend/app/dexa_parser.py",
        "backend/app/avatar_generator.py",
        "backend/app/models.py",
        "backend/requirements.txt",
    ]
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing backend files: {', '.join(missing)}")
        return False
    print("✅ Backend structure complete")
    return True

def check_frontend_structure():
    """Check if frontend files exist."""
    required_files = [
        "frontend/package.json",
        "frontend/src/App.jsx",
        "frontend/src/components/AvatarViewer.jsx",
        "frontend/src/components/UploadForm.jsx",
    ]
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing frontend files: {', '.join(missing)}")
        return False
    print("✅ Frontend structure complete")
    return True

def check_sample_data():
    """Check if sample DEXA PDFs exist."""
    sample_dir = Path("data/samples")
    pdfs = list(sample_dir.glob("*.pdf"))
    if not pdfs:
        print("⚠️  No sample DEXA PDFs found in data/samples/")
        return False
    print(f"✅ Found {len(pdfs)} sample DEXA PDF(s)")
    return True

def check_directories():
    """Check if required directories exist."""
    required_dirs = ["backend", "frontend", "data", "output", "models"]
    missing = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing.append(dir_name)
    
    if missing:
        print(f"⚠️  Missing directories (will be created): {', '.join(missing)}")
        for dir_name in missing:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
    print("✅ Required directories exist")
    return True

def main():
    print("=" * 60)
    print("DEXA to 3D Avatar - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Backend Structure", check_backend_structure),
        ("Frontend Structure", check_frontend_structure),
        ("Backend Dependencies", check_backend_dependencies),
        ("Directories", check_directories),
        ("Sample Data", check_sample_data),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"Checking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
        print()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("✅ All checks passed! Ready to test the pipeline.")
        print()
        print("Next steps:")
        print("1. Start backend: cd backend && uvicorn app.main:app --reload")
        print("2. Start frontend: cd frontend && npm run dev")
        print("3. Open http://localhost:3000 and test")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("- Install backend deps: cd backend && pip install -r requirements.txt")
        print("- Install frontend deps: cd frontend && npm install")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

