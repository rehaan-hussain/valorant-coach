#!/usr/bin/env python3
"""
Setup script for Valorant AI Coach
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
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "logs",
        "data",
        "models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")
    
    return True

def run_tests():
    """Run installation tests"""
    print("\n🧪 Running tests...")
    
    if not run_command(f"{sys.executable} test_installation.py", "Running installation tests"):
        return False
    
    return True

def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Valorant AI Coach Setup Complete!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Test the installation:")
    print("   python test_installation.py")
    
    print("\n2. Run the demo to see the system in action:")
    print("   python demo.py")
    
    print("\n3. Start the main application:")
    print("   python main.py")
    print("   or")
    print("   python run_streamlit.py")
    
    print("\n4. Open your browser and go to:")
    print("   http://localhost:8501")
    
    print("\n📖 Documentation:")
    print("   Read README.md for detailed usage instructions")
    
    print("\n⚠️  Important Notes:")
    print("   - Make sure Valorant is running for real gameplay analysis")
    print("   - The system captures your screen, so ensure you're comfortable with this")
    print("   - This is an MVP - some features may need refinement")
    
    print("\n🎮 Happy gaming and improving!")

def main():
    """Main setup function"""
    print("🎮 Valorant AI Coach Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return 1
    
    # Create directories
    if not create_directories():
        print("\n❌ Setup failed: Could not create directories")
        return 1
    
    # Run tests
    if not run_tests():
        print("\n❌ Setup failed: Tests did not pass")
        return 1
    
    # Show next steps
    show_next_steps()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())