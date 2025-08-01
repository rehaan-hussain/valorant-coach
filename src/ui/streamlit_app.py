"""
Main Streamlit application for Valorant AI Coach
"""

import streamlit as st
import time
import threading
import cv2
import numpy as np
from typing import Dict, List
import logging

# Import our modules
from src.capture import ScreenCapture, FrameProcessor
from ..analysis import GameAnalyzer
from ..coaching import Coach, PlayerProfile

logger = logging.getLogger(__name__)

class ValorantCoachApp:
    """Main Streamlit application for Valorant coaching"""
    
    def __init__(self):
        """Initialize the application"""
        self.capture = None
        self.processor = None
        self.analyzer = None
        self.coach = None
        self.is_running = False
        self.analysis_thread = None
        
        # Session state
        if 'capture_running' not in st.session_state:
            st.session_state.capture_running = False
        if 'current_tips' not in st.session_state:
            st.session_state.current_tips = []
        if 'performance_data' not in st.session_state:
            st.session_state.performance_data = []
        if 'session_stats' not in st.session_state:
            st.session_state.session_stats = {}
    
    def setup_page(self):
        """Setup the Streamlit page configuration"""
        st.set_page_config(
            page_title="Valorant AI Coach",
            page_icon="🎮",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🎮 Valorant AI Coach")
        st.markdown("### Your Personal AI Gaming Coach")
        
        # Add CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #FF4655, #0F1419);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .tip-card {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #FF4655;
            margin: 0.5rem 0;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def sidebar_setup(self):
        """Setup the sidebar with controls"""
        st.sidebar.title("🎯 Coach Controls")
        
        # Player Profile Section
        st.sidebar.header("👤 Player Profile")
        
        skill_level = st.sidebar.selectbox(
            "Skill Level",
            ["beginner", "intermediate", "advanced"],
            index=0
        )
        
        primary_role = st.sidebar.selectbox(
            "Primary Role",
            ["duelist", "sentinel", "initiator", "controller"],
            index=0
        )
        
        # Capture Settings
        st.sidebar.header("📹 Capture Settings")
        
        monitor_id = st.sidebar.selectbox(
            "Monitor",
            [1, 2, 3],
            index=0,
            help="Select which monitor to capture"
        )
        
        fps = st.sidebar.slider(
            "FPS",
            min_value=15,
            max_value=60,
            value=30,
            help="Frames per second for capture"
        )
        
        # Control Buttons
        st.sidebar.header("🎮 Controls")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("▶️ Start Coaching", type="primary"):
                self.start_coaching(monitor_id, fps, skill_level, primary_role)
        
        with col2:
            if st.button("⏹️ Stop Coaching"):
                self.stop_coaching()
        
        # Session Info
        if st.session_state.capture_running:
            st.sidebar.header("📊 Session Info")
            st.sidebar.metric("Frames Processed", st.session_state.session_stats.get('frames_processed', 0))
            st.sidebar.metric("Tips Given", len(st.session_state.current_tips))
            
            if st.sidebar.button("📈 View Detailed Stats"):
                self.show_detailed_stats()
    
    def start_coaching(self, monitor_id: int, fps: int, skill_level: str, primary_role: str):
        """Start the coaching session"""
        try:
            # Initialize components
            self.capture = ScreenCapture(monitor_id=monitor_id, fps=fps)
            self.processor = FrameProcessor()
            self.analyzer = GameAnalyzer()
            
            # Create player profile
            player_profile = PlayerProfile(
                skill_level=skill_level,
                primary_role=primary_role,
                strengths=["enthusiasm", "willingness to learn"],
                weaknesses=["aim", "positioning", "game sense"],
                goals=["improve overall gameplay", "reach higher rank"],
                playtime_hours=0
            )
            
            self.coach = Coach(player_profile)
            
            # Start capture
            self.capture.start_capture(callback=self.frame_callback)
            self.is_running = True
            st.session_state.capture_running = True
            
            st.success("🎮 Coaching session started! Play Valorant and receive real-time tips.")
            
        except Exception as e:
            st.error(f"❌ Failed to start coaching: {str(e)}")
            logger.error(f"Failed to start coaching: {e}")
    
    def stop_coaching(self):
        """Stop the coaching session"""
        try:
            if self.capture:
                self.capture.stop_capture()
            
            self.is_running = False
            st.session_state.capture_running = False
            
            st.success("⏹️ Coaching session stopped.")
            
        except Exception as e:
            st.error(f"❌ Error stopping coaching: {str(e)}")
            logger.error(f"Error stopping coaching: {e}")
    
    def frame_callback(self, frame):
        """Callback for each captured frame"""
        if not self.is_running:
            return
        
        try:
            # Process frame
            frame_data = self.processor.process_frame(frame)
            
            # Analyze frame
            analysis = self.analyzer.process_frame_data(frame_data)
            
            # Generate coaching tips
            if analysis:
                tips = self.coach.process_analysis(analysis)
                
                # Update session state
                st.session_state.current_tips.extend(tips)
                st.session_state.performance_data.append(analysis.get('performance'))
                st.session_state.session_stats = analysis.get('session_stats', {})
                
                # Keep only recent tips
                if len(st.session_state.current_tips) > 10:
                    st.session_state.current_tips = st.session_state.current_tips[-10:]
                
        except Exception as e:
            logger.error(f"Error in frame callback: {e}")
    
    def main_content(self):
        """Main content area"""
        if not st.session_state.capture_running:
            self.show_welcome_screen()
        else:
            self.show_coaching_interface()
    
    def show_welcome_screen(self):
        """Show welcome screen when not coaching"""
        st.markdown("""
        <div class="main-header">
            <h1>🎮 Welcome to Valorant AI Coach</h1>
            <p>Your personal AI assistant to improve your Valorant gameplay</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Real-time Analysis</h3>
                <p>Get instant feedback on your gameplay mechanics</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Performance Tracking</h3>
                <p>Monitor your improvement over time</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>🎓 Personalized Tips</h3>
                <p>Receive coaching advice tailored to your skill level</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Configure your profile** in the sidebar
        2. **Select your monitor** and preferred FPS
        3. **Click 'Start Coaching'** to begin
        4. **Play Valorant** and receive real-time tips
        5. **Review your performance** and improvement areas
        
        ### 🎯 What We Analyze
        
        - **Crosshair Placement**: Accuracy and consistency
        - **Movement**: Efficiency and positioning
        - **Game Sense**: Decision making and awareness
        - **Mechanics**: Aim, recoil control, and reactions
        - **Positioning**: Map awareness and team coordination
        """)
    
    def show_coaching_interface(self):
        """Show the main coaching interface"""
        # Performance Overview
        st.header("📊 Performance Overview")
        
        if st.session_state.performance_data:
            latest_performance = st.session_state.performance_data[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Accuracy",
                    f"{latest_performance.accuracy:.1%}",
                    help="Based on crosshair placement and target acquisition"
                )
            
            with col2:
                st.metric(
                    "Crosshair Placement",
                    f"{latest_performance.crosshair_placement:.1%}",
                    help="Consistency of crosshair positioning"
                )
            
            with col3:
                st.metric(
                    "Movement Efficiency",
                    f"{latest_performance.movement_efficiency:.1%}",
                    help="Quality of movement and positioning"
                )
            
            with col4:
                st.metric(
                    "Overall Score",
                    f"{latest_performance.overall_score:.1%}",
                    help="Combined performance score"
                )
        
        # Real-time Tips
        st.header("💡 Real-time Coaching Tips")
        
        if st.session_state.current_tips:
            for tip in st.session_state.current_tips[-3:]:  # Show last 3 tips
                st.markdown(f"""
                <div class="tip-card">
                    <strong>🎯 {tip.category.replace('_', ' ').title()}</strong><br>
                    {tip.message}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎮 Start playing Valorant to receive coaching tips!")
        
        # Performance Charts
        if len(st.session_state.performance_data) > 5:
            st.header("📈 Performance Trends")
            
            # Create performance chart
            import pandas as pd
            import plotly.express as px
            
            df = pd.DataFrame([
                {
                    'Time': i,
                    'Accuracy': p.accuracy,
                    'Crosshair Placement': p.crosshair_placement,
                    'Movement Efficiency': p.movement_efficiency,
                    'Overall Score': p.overall_score
                }
                for i, p in enumerate(st.session_state.performance_data)
            ])
            
            fig = px.line(df, x='Time', y=['Accuracy', 'Crosshair Placement', 'Movement Efficiency', 'Overall Score'],
                         title="Performance Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        # Training Recommendations
        if self.coach:
            st.header("🎓 Training Recommendations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 Generate Training Plan"):
                    training_plan = self.coach.generate_training_plan()
                    st.session_state.training_plan = training_plan
            
            with col2:
                if st.button("📊 View Detailed Analysis"):
                    self.show_detailed_analysis()
            
            if 'training_plan' in st.session_state:
                plan = st.session_state.training_plan
                st.subheader("Your Personalized Training Plan")
                
                for area in plan['focus_areas']:
                    with st.expander(f"🎯 {area.replace('_', ' ').title()}"):
                        st.write(f"**Goal:** {plan['goals'][plan['focus_areas'].index(area)]}")
                        st.write("**Exercises:**")
                        for exercise in plan['exercises'][area]:
                            st.write(f"• {exercise}")
    
    def show_detailed_stats(self):
        """Show detailed session statistics"""
        st.header("📊 Detailed Session Statistics")
        
        if self.analyzer:
            summary = self.analyzer.get_session_summary()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Session Duration", f"{summary['session_duration']:.1f}s")
                st.metric("Frames Processed", summary['frames_processed'])
                st.metric("Events Detected", summary['events_detected'])
            
            with col2:
                if summary['current_performance']:
                    perf = summary['current_performance']
                    st.metric("Current Accuracy", f"{perf.accuracy:.1%}")
                    st.metric("Current Crosshair", f"{perf.crosshair_placement:.1%}")
                    st.metric("Current Movement", f"{perf.movement_efficiency:.1%}")
        
        if self.coach:
            coaching_stats = self.coach.get_coaching_stats()
            
            st.subheader("Coaching Statistics")
            st.metric("Total Tips Given", coaching_stats['total_tips_given'])
            st.metric("Session Tips", coaching_stats['session_tips'])
            
            st.subheader("Player Profile")
            profile = coaching_stats['player_profile']
            st.write(f"**Skill Level:** {profile.skill_level}")
            st.write(f"**Primary Role:** {profile.primary_role}")
            st.write(f"**Strengths:** {', '.join(profile.strengths)}")
            st.write(f"**Weaknesses:** {', '.join(profile.weaknesses)}")
    
    def show_detailed_analysis(self):
        """Show detailed analysis of current session"""
        st.header("🔍 Detailed Analysis")
        
        if self.analyzer:
            summary = self.analyzer.get_session_summary()
            
            # Performance breakdown
            st.subheader("Performance Breakdown")
            
            if summary['performance_history']:
                import pandas as pd
                
                df = pd.DataFrame([
                    {
                        'Time': i,
                        'Accuracy': p.accuracy,
                        'Crosshair Placement': p.crosshair_placement,
                        'Movement Efficiency': p.movement_efficiency,
                        'Game Sense': p.game_sense,
                        'Overall Score': p.overall_score
                    }
                    for i, p in enumerate(summary['performance_history'])
                ])
                
                # Show performance heatmap
                import plotly.express as px
                
                fig = px.imshow(
                    df[['Accuracy', 'Crosshair Placement', 'Movement Efficiency', 'Game Sense']].T,
                    title="Performance Heatmap",
                    labels=dict(x="Time", y="Skill", color="Score")
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def run(self):
        """Run the Streamlit application"""
        self.setup_page()
        self.sidebar_setup()
        self.main_content()

def create_app():
    """Create and run the Streamlit app"""
    app = ValorantCoachApp()
    app.run()

if __name__ == "__main__":
    create_app()