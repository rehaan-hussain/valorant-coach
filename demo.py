#!/usr/bin/env python3
"""
Demo script for Valorant AI Coach
This demonstrates the system's capabilities without requiring actual gameplay
"""

import sys
import time
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.capture.frame_processor import FrameProcessor, GameElement, CrosshairInfo
from src.analysis.game_analyzer import GameAnalyzer, PerformanceMetrics
from src.coaching.coach import Coach, PlayerProfile
from src.analysis.skill_assessor import SkillAssessor

def create_demo_frame(width=1920, height=1080):
    """Create a demo frame for testing"""
    # Create a simple demo frame
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add some demo elements
    # Crosshair (center)
    center_x, center_y = width // 2, height // 2
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), 2)
    
    # Demo enemy (red rectangle)
    enemy_x, enemy_y = center_x + 200, center_y - 50
    cv2.rectangle(frame, (enemy_x-20, enemy_y-40), (enemy_x+20, enemy_y+40), (0, 0, 255), -1)
    
    # UI elements (bottom corners)
    cv2.rectangle(frame, (0, height-100), (200, height), (0, 255, 0), -1)  # Health
    cv2.rectangle(frame, (width-200, height-100), (width, height), (255, 255, 255), -1)  # Ammo
    
    return frame

def run_demo():
    """Run the demo"""
    print("🎮 Valorant AI Coach Demo")
    print("=" * 50)
    
    # Initialize components
    processor = FrameProcessor()
    analyzer = GameAnalyzer()
    
    # Create player profile
    player_profile = PlayerProfile(
        skill_level="beginner",
        primary_role="duelist",
        strengths=["enthusiasm", "willingness to learn"],
        weaknesses=["aim", "positioning", "game sense"],
        goals=["improve overall gameplay", "reach higher rank"],
        playtime_hours=0
    )
    
    coach = Coach(player_profile)
    skill_assessor = SkillAssessor()
    
    print("✅ Components initialized")
    print()
    
    # Simulate gameplay analysis
    print("🎯 Simulating gameplay analysis...")
    print()
    
    for i in range(10):
        # Create demo frame
        frame = create_demo_frame()
        
        # Process frame
        frame_data = processor.process_frame(frame)
        
        # Analyze frame
        analysis = analyzer.process_frame_data(frame_data)
        
        # Generate coaching tips
        tips = coach.process_analysis(analysis)
        
        # Display results
        print(f"Frame {i+1}:")
        
        if analysis.get('performance'):
            perf = analysis['performance']
            print(f"  📊 Performance: Accuracy={perf.accuracy:.1%}, "
                  f"Crosshair={perf.crosshair_placement:.1%}, "
                  f"Movement={perf.movement_efficiency:.1%}")
        
        if tips:
            for tip in tips:
                print(f"  💡 Tip: {tip.message}")
        
        print()
        time.sleep(0.5)
    
    # Show final analysis
    print("📈 Final Analysis")
    print("-" * 30)
    
    summary = analyzer.get_session_summary()
    print(f"Session Duration: {summary['session_duration']:.1f}s")
    print(f"Frames Processed: {summary['frames_processed']}")
    print(f"Events Detected: {summary['events_detected']}")
    
    if summary['current_performance']:
        perf = summary['current_performance']
        print(f"Final Performance Score: {perf.overall_score:.1%}")
    
    print()
    
    # Skill assessment
    print("🎓 Skill Assessment")
    print("-" * 30)
    
    if summary['current_performance']:
        performance_data = {
            'accuracy': summary['current_performance'].accuracy,
            'crosshair_placement': summary['current_performance'].crosshair_placement,
            'movement_efficiency': summary['current_performance'].movement_efficiency,
            'game_sense': summary['current_performance'].game_sense,
            'reaction_time': summary['current_performance'].reaction_time
        }
        
        assessments = skill_assessor.assess_skills(performance_data)
        overall_level = skill_assessor.get_overall_skill_level(assessments)
        
        print(f"Overall Skill Level: {overall_level}")
        print()
        
        for skill_name, assessment in assessments.items():
            print(f"{skill_name.replace('_', ' ').title()}: {assessment.score:.1%}")
            if assessment.improvement_needed:
                print(f"  ⚠️  Needs improvement")
                for rec in assessment.recommendations[:2]:
                    print(f"  💡 {rec}")
            print()
    
    # Training plan
    print("📋 Training Plan")
    print("-" * 30)
    
    training_plan = coach.generate_training_plan()
    print(f"Focus Areas: {', '.join(training_plan['focus_areas'])}")
    print(f"Duration: {training_plan['duration']}")
    print(f"Frequency: {training_plan['frequency']}")
    print()
    
    for area in training_plan['focus_areas']:
        print(f"🎯 {area.replace('_', ' ').title()}:")
        print(f"  Goal: {training_plan['goals'][training_plan['focus_areas'].index(area)]}")
        print("  Exercises:")
        for exercise in training_plan['exercises'][area][:2]:
            print(f"    • {exercise}")
        print()
    
    # Coaching statistics
    print("📊 Coaching Statistics")
    print("-" * 30)
    
    coaching_stats = coach.get_coaching_stats()
    print(f"Total Tips Given: {coaching_stats['total_tips_given']}")
    print(f"Session Tips: {coaching_stats['session_tips']}")
    print(f"Player Skill Level: {coaching_stats['player_profile'].skill_level}")
    print(f"Primary Role: {coaching_stats['player_profile'].primary_role}")
    
    print()
    print("🎉 Demo completed! This shows the core functionality of the Valorant AI Coach.")
    print("To use with real gameplay, run: python main.py")

if __name__ == "__main__":
    # Import cv2 for demo frame creation
    import cv2
    run_demo()