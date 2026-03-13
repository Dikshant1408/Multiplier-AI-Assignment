"""
Setup script for easy project initialization
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command"""
    print(f"\n{'='*60}")
    print(f"Running: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=False
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("DATA ANALYSIS DASHBOARD - SETUP")
    print("="*60)
    
    # Install Python dependencies
    print("\n1. Installing Python dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r backend/requirements.txt"):
        print("Failed to install Python dependencies")
        return
    
    # Install pytest for tests
    print("\n2. Installing pytest...")
    if not run_command(f"{sys.executable} -m pip install pytest"):
        print("Failed to install pytest")
    
    # Run data cleaning
    print("\n3. Running data cleaning...")
    if not run_command(f"{sys.executable} clean_data.py"):
        print("Failed to clean data")
        return
    
    # Run data analysis
    print("\n4. Running data analysis...")
    if not run_command(f"{sys.executable} analyze.py"):
        print("Failed to analyze data")
        return
    
    # Install frontend dependencies
    print("\n5. Installing frontend dependencies...")
    frontend_path = Path('frontend')
    if not run_command("npm install", cwd=frontend_path):
        print("Failed to install frontend dependencies")
        print("You may need to install Node.js and npm first")
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Start backend:  cd backend && uvicorn main:app --reload")
    print("2. Start frontend: cd frontend && npm start")
    print("3. Run tests:      pytest tests/ -v")
    print("\n")


if __name__ == '__main__':
    main()
