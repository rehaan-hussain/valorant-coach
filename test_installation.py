#!/usr/bin/env python3
"""
Test script to verify Valorant AI Coach installation
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        # Test core modules
        from src.capture import ScreenCapture, FrameProcessor
        print("✅ Capture modules imported successfully")
        
        from src.analysis import GameAnalyzer, SkillAssessor, BehaviorAnalyzer
        print("✅ Analysis modules imported successfully")
        
        from src.coaching import Coach, PlayerProfile
        print("✅ Coaching modules imported successfully")
        
        from src.utils import Config
        print("✅ Utils modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test frame processor
        from src.capture.frame_processor import FrameProcessor
        processor = FrameProcessor()
        print("✅ Frame processor initialized")
        
        # Test game analyzer
        from src.analysis.game_analyzer import GameAnalyzer
        analyzer = GameAnalyzer()
        print("✅ Game analyzer initialized")
        
        # Test coach
        from src.coaching.coach import Coach, PlayerProfile
        profile = PlayerProfile(
            skill_level="beginner",
            primary_role="duelist",
            strengths=["enthusiasm"],
            weaknesses=["aim"],
            goals=["improve"],
            playtime_hours=0
        )
        coach = Coach(profile)
        print("✅ Coach initialized")
        
        # Test skill assessor
        from src.analysis.skill_assessor import SkillAssessor
        assessor = SkillAssessor()
        print("✅ Skill assessor initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    print("\n🧪 Testing dependencies...")
    
    required_packages = [
        'opencv-python',
        'numpy',
        'streamlit',
        'mss',
        'pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'numpy':
                import numpy
            elif package == 'streamlit':
                import streamlit
            elif package == 'mss':
                import mss
            elif package == 'pillow':
                import PIL
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🎮 Valorant AI Coach - Installation Test")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test functionality
    func_ok = test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Functionality: {'✅ PASS' if func_ok else '❌ FAIL'}")
    
    if deps_ok and imports_ok and func_ok:
        print("\n🎉 All tests passed! Valorant AI Coach is ready to use.")
        print("\nTo run the application:")
        print("  python main.py")
        print("  or")
        print("  python run_streamlit.py")
        print("\nTo run the demo:")
        print("  python demo.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())