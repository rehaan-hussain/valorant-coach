#!/usr/bin/env python3
"""
Test script to verify Valorant AI Coach installation
"""

import sys
import os
from pathlib import Path

# --- Windows console safety: force UTF-8 or fall back to plain text ---
import os, sys
def _safe_print(s: str):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        print(s)
    except UnicodeEncodeError:
        # Fallback: strip non-ASCII characters
        print(s.encode("ascii", "ignore").decode())

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    print("[INFO] Testing imports...")
    
    try:
        # Test core modules
        from src.capture import ScreenCapture, FrameProcessor
        print("[SUCCESS] Capture modules imported successfully")
        
        from src.analysis import GameAnalyzer, SkillAssessor, BehaviorAnalyzer
        print("[SUCCESS] Analysis modules imported successfully")
        
        from src.coaching import Coach, PlayerProfile
        print("[SUCCESS] Coaching modules imported successfully")
        
        from src.utils import Config
        print("[SUCCESS] Utils modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n[INFO] Testing basic functionality...")
    
    try:
        # Test frame processor
        from src.capture.frame_processor import FrameProcessor
        processor = FrameProcessor()
        print("[SUCCESS] Frame processor initialized")
        
        # Test game analyzer
        from src.analysis.game_analyzer import GameAnalyzer
        analyzer = GameAnalyzer()
        print("[SUCCESS] Game analyzer initialized")
        
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
        print("[SUCCESS] Coach initialized")
        
        # Test skill assessor
        from src.analysis.skill_assessor import SkillAssessor
        assessor = SkillAssessor()
        print("[SUCCESS] Skill assessor initialized")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Functionality test error: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    print("\n[INFO] Testing dependencies...")
    
    # Core dependencies (required)
    core_packages = [
        ('opencv-python', 'cv2'),
        ('numpy', 'numpy'),
        ('streamlit', 'streamlit'),
        ('mss', 'mss'),
        ('pillow', 'PIL')
    ]
    
    # Optional dependencies
    optional_packages = [
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('plotly', 'plotly'),
        ('scikit-learn', 'sklearn'),
        ('tensorflow', 'tensorflow'),
        ('torch', 'torch'),
        ('ultralytics', 'ultralytics')
    ]
    
    missing_core = []
    missing_optional = []
    
    # Test core packages
    print("[INFO] Core dependencies:")
    for package_name, import_name in core_packages:
        try:
            __import__(import_name)
            print(f"  [SUCCESS] {package_name} available")
        except ImportError:
            print(f"  [ERROR] {package_name} missing")
            missing_core.append(package_name)
    
    # Test optional packages
    print("\n[INFO] Optional dependencies:")
    for package_name, import_name in optional_packages:
        try:
            __import__(import_name)
            print(f"  [SUCCESS] {package_name} available")
        except ImportError:
            print(f"  [WARNING] {package_name} missing (optional)")
            missing_optional.append(package_name)
    
    if missing_core:
        print(f"\n[ERROR] Missing core packages: {', '.join(missing_core)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n[WARNING] Missing optional packages: {', '.join(missing_optional)}")
        print("These are not required for basic functionality")
    
    return True

def test_demo_functionality():
    """Test if demo can run"""
    print("\n[INFO] Testing demo functionality...")
    
    try:
        # Test if we can create a simple demo frame
        import numpy as np
        import cv2
        
        # Create a simple test frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 240), 50, (0, 255, 0), 2)
        
        print("[SUCCESS] Demo frame creation works")
        return True
        
    except Exception as e:
        print(f"[ERROR] Demo functionality error: {e}")
        return False

def main():
    """Run all tests"""
    _safe_print("🎮 Valorant AI Coach - Installation Test")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test functionality
    func_ok = test_basic_functionality()
    
    # Test demo functionality
    demo_ok = test_demo_functionality()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Dependencies: {'[PASS]' if deps_ok else '[FAIL]'}")
    print(f"Imports: {'[PASS]' if imports_ok else '[FAIL]'}")
    print(f"Functionality: {'[PASS]' if func_ok else '[FAIL]'}")
    print(f"Demo: {'[PASS]' if demo_ok else '[FAIL]'}")
    
    if deps_ok and imports_ok and func_ok:
        print("\n[SUCCESS] Core functionality is working! Valorant AI Coach is ready to use.")
        print("\nTo run the application:")
        print("  python main.py")
        print("  or")
        print("  python run_streamlit.py")
        print("\nTo run the demo:")
        print("  python demo.py")
        
        if not demo_ok:
            print("\n[WARNING] Demo functionality has issues, but core features should work")
    else:
        print("\n[ERROR] Some tests failed. Please check the errors above.")
        print("\nTry manual installation:")
        print("   See INSTALL.md for detailed instructions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())