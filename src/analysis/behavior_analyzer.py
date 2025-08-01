"""
Behavior analysis module for understanding player patterns
"""

import numpy as np
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class BehaviorPattern:
    """Represents a detected behavior pattern"""
    pattern_type: str
    confidence: float
    frequency: float
    description: str
    impact: str  # "positive", "negative", "neutral"

class BehaviorAnalyzer:
    """
    Analyzes player behavior patterns and tendencies
    """
    
    def __init__(self, history_size: int = 1000):
        """
        Initialize behavior analyzer
        
        Args:
            history_size: Number of frames to keep in history
        """
        self.history_size = history_size
        self.behavior_history = deque(maxlen=history_size)
        self.patterns = {}
        
        logger.info("Behavior analyzer initialized")
    
    def analyze_behavior(self, frame_data: Dict) -> Dict:
        """
        Analyze behavior patterns in current frame
        
        Args:
            frame_data: Current frame analysis data
            
        Returns:
            Behavior analysis results
        """
        if not frame_data:
            return {}
        
        # Store in history
        self.behavior_history.append(frame_data)
        
        # Analyze patterns
        patterns = self._detect_patterns()
        
        # Analyze tendencies
        tendencies = self._analyze_tendencies()
        
        # Generate insights
        insights = self._generate_behavior_insights(patterns, tendencies)
        
        return {
            'patterns': patterns,
            'tendencies': tendencies,
            'insights': insights
        }
    
    def _detect_patterns(self) -> List[BehaviorPattern]:
        """Detect behavior patterns from history"""
        patterns = []
        
        if len(self.behavior_history) < 10:
            return patterns
        
        # Analyze crosshair movement patterns
        crosshair_pattern = self._analyze_crosshair_patterns()
        if crosshair_pattern:
            patterns.append(crosshair_pattern)
        
        # Analyze movement patterns
        movement_pattern = self._analyze_movement_patterns()
        if movement_pattern:
            patterns.append(movement_pattern)
        
        # Analyze engagement patterns
        engagement_pattern = self._analyze_engagement_patterns()
        if engagement_pattern:
            patterns.append(engagement_pattern)
        
        return patterns
    
    def _analyze_crosshair_patterns(self) -> Optional[BehaviorPattern]:
        """Analyze crosshair movement patterns"""
        if len(self.behavior_history) < 20:
            return None
        
        # Extract crosshair positions
        positions = []
        for frame in list(self.behavior_history)[-20:]:
            if frame.get('crosshair') and frame['crosshair'].is_visible:
                positions.append(frame['crosshair'].position)
        
        if len(positions) < 10:
            return None
        
        # Calculate movement patterns
        movements = []
        for i in range(1, len(positions)):
            dx = positions[i][0] - positions[i-1][0]
            dy = positions[i][1] - positions[i-1][1]
            movements.append(np.sqrt(dx*dx + dy*dy))
        
        avg_movement = np.mean(movements)
        movement_variance = np.var(movements)
        
        # Determine pattern type
        if avg_movement < 5:
            return BehaviorPattern(
                pattern_type="steady_aim",
                confidence=0.8,
                frequency=0.7,
                description="Player maintains steady crosshair position",
                impact="positive"
            )
        elif avg_movement > 20:
            return BehaviorPattern(
                pattern_type="jittery_aim",
                confidence=0.7,
                frequency=0.6,
                description="Player has jittery crosshair movement",
                impact="negative"
            )
        elif movement_variance > 100:
            return BehaviorPattern(
                pattern_type="inconsistent_aim",
                confidence=0.6,
                frequency=0.5,
                description="Player has inconsistent crosshair movement",
                impact="negative"
            )
        
        return None
    
    def _analyze_movement_patterns(self) -> Optional[BehaviorPattern]:
        """Analyze movement patterns"""
        if len(self.behavior_history) < 20:
            return None
        
        # Extract movement data
        movements = []
        for frame in list(self.behavior_history)[-20:]:
            if frame.get('movement'):
                movements.append(frame['movement'])
        
        if len(movements) < 10:
            return None
        
        # Analyze movement efficiency
        moving_frames = sum(1 for m in movements if m.get('is_moving', False))
        movement_ratio = moving_frames / len(movements)
        
        avg_magnitude = np.mean([m.get('movement_magnitude', 0) for m in movements])
        
        if movement_ratio > 0.8:
            return BehaviorPattern(
                pattern_type="excessive_movement",
                confidence=0.7,
                frequency=movement_ratio,
                description="Player moves too frequently",
                impact="negative"
            )
        elif movement_ratio < 0.2:
            return BehaviorPattern(
                pattern_type="stationary_play",
                confidence=0.6,
                frequency=1 - movement_ratio,
                description="Player stays stationary too often",
                impact="neutral"
            )
        elif avg_magnitude > 10:
            return BehaviorPattern(
                pattern_type="erratic_movement",
                confidence=0.6,
                frequency=0.5,
                description="Player has erratic movement patterns",
                impact="negative"
            )
        
        return None
    
    def _analyze_engagement_patterns(self) -> Optional[BehaviorPattern]:
        """Analyze engagement patterns"""
        if len(self.behavior_history) < 20:
            return None
        
        # Count enemy detections
        enemy_detections = 0
        for frame in list(self.behavior_history)[-20:]:
            if frame.get('enemies') and len(frame['enemies']) > 0:
                enemy_detections += 1
        
        detection_ratio = enemy_detections / len(self.behavior_history)
        
        if detection_ratio > 0.5:
            return BehaviorPattern(
                pattern_type="aggressive_play",
                confidence=0.7,
                frequency=detection_ratio,
                description="Player engages enemies frequently",
                impact="positive"
            )
        elif detection_ratio < 0.1:
            return BehaviorPattern(
                pattern_type="passive_play",
                confidence=0.6,
                frequency=1 - detection_ratio,
                description="Player avoids engagements",
                impact="neutral"
            )
        
        return None
    
    def _analyze_tendencies(self) -> Dict:
        """Analyze player tendencies"""
        if len(self.behavior_history) < 10:
            return {}
        
        tendencies = {
            'aim_style': self._determine_aim_style(),
            'movement_style': self._determine_movement_style(),
            'engagement_style': self._determine_engagement_style(),
            'positioning_style': self._determine_positioning_style()
        }
        
        return tendencies
    
    def _determine_aim_style(self) -> str:
        """Determine player's aim style"""
        # Analyze crosshair placement and movement
        crosshair_positions = []
        for frame in list(self.behavior_history)[-30:]:
            if frame.get('crosshair') and frame['crosshair'].is_visible:
                crosshair_positions.append(frame['crosshair'].position)
        
        if len(crosshair_positions) < 5:
            return "unknown"
        
        # Calculate variance in crosshair position
        positions = np.array(crosshair_positions)
        variance = np.var(positions, axis=0).mean()
        
        if variance < 50:
            return "steady"
        elif variance < 200:
            return "controlled"
        else:
            return "erratic"
    
    def _determine_movement_style(self) -> str:
        """Determine player's movement style"""
        movement_data = []
        for frame in list(self.behavior_history)[-30:]:
            if frame.get('movement'):
                movement_data.append(frame['movement'])
        
        if len(movement_data) < 5:
            return "unknown"
        
        moving_ratio = sum(1 for m in movement_data if m.get('is_moving', False)) / len(movement_data)
        avg_magnitude = np.mean([m.get('movement_magnitude', 0) for m in movement_data])
        
        if moving_ratio < 0.2:
            return "stationary"
        elif moving_ratio > 0.8:
            return "hyperactive"
        elif avg_magnitude > 8:
            return "erratic"
        else:
            return "controlled"
    
    def _determine_engagement_style(self) -> str:
        """Determine player's engagement style"""
        enemy_counts = []
        for frame in list(self.behavior_history)[-30:]:
            enemy_counts.append(len(frame.get('enemies', [])))
        
        if len(enemy_counts) < 5:
            return "unknown"
        
        avg_enemies = np.mean(enemy_counts)
        max_enemies = max(enemy_counts)
        
        if avg_enemies > 1.5:
            return "aggressive"
        elif max_enemies > 2:
            return "opportunistic"
        elif avg_enemies < 0.5:
            return "passive"
        else:
            return "balanced"
    
    def _determine_positioning_style(self) -> str:
        """Determine player's positioning style"""
        # This would require more sophisticated analysis
        # For now, return a placeholder
        return "standard"
    
    def _generate_behavior_insights(self, patterns: List[BehaviorPattern], tendencies: Dict) -> List[str]:
        """Generate insights from behavior analysis"""
        insights = []
        
        # Pattern-based insights
        for pattern in patterns:
            if pattern.impact == "negative":
                if pattern.pattern_type == "jittery_aim":
                    insights.append("Your aim is jittery. Try to stay calm and control your mouse movements.")
                elif pattern.pattern_type == "excessive_movement":
                    insights.append("You're moving too much. Try to stay still when aiming and shooting.")
                elif pattern.pattern_type == "erratic_movement":
                    insights.append("Your movement is erratic. Practice smooth, controlled movement.")
        
        # Tendency-based insights
        aim_style = tendencies.get('aim_style', 'unknown')
        if aim_style == "erratic":
            insights.append("Your aim style is erratic. Focus on smooth, controlled movements.")
        
        movement_style = tendencies.get('movement_style', 'unknown')
        if movement_style == "hyperactive":
            insights.append("You move too frequently. Learn to stay still when necessary.")
        
        engagement_style = tendencies.get('engagement_style', 'unknown')
        if engagement_style == "passive":
            insights.append("You're too passive. Look for opportunities to engage enemies.")
        elif engagement_style == "aggressive":
            insights.append("You're very aggressive. Make sure to coordinate with your team.")
        
        return insights[:3]  # Limit to top 3 insights
    
    def get_behavior_summary(self) -> Dict:
        """Get summary of behavior analysis"""
        return {
            'patterns_detected': len(self.patterns),
            'history_size': len(self.behavior_history),
            'analysis_confidence': 0.7  # Placeholder
        }