"""
Main game analyzer for Valorant gameplay evaluation
"""

import numpy as np
import time
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class GameEvent:
    """Represents a significant game event"""
    event_type: str
    timestamp: float
    confidence: float
    data: Dict
    position: Optional[Tuple[int, int]] = None

@dataclass
class PerformanceMetrics:
    """Performance metrics for a session"""
    accuracy: float
    reaction_time: float
    crosshair_placement: float
    movement_efficiency: float
    game_sense: float
    overall_score: float

class GameAnalyzer:
    """
    Main analyzer for Valorant gameplay patterns and performance
    """
    
    def __init__(self, session_duration: int = 300):  # 5 minutes default
        """
        Initialize game analyzer
        
        Args:
            session_duration: Duration to keep data in seconds
        """
        self.session_duration = session_duration
        self.start_time = time.time()
        
        # Data storage
        self.frame_data = deque(maxlen=1800)  # 30 FPS * 60 seconds
        self.events = deque(maxlen=1000)
        self.performance_history = deque(maxlen=100)
        
        # Analysis state
        self.current_session = {
            'start_time': self.start_time,
            'frames_processed': 0,
            'events_detected': 0,
            'performance_score': 0.0
        }
        
        # Thresholds for analysis
        self.accuracy_threshold = 0.7
        self.reaction_threshold = 0.3  # seconds
        self.movement_threshold = 0.5
        
        logger.info("Game analyzer initialized")
    
    def process_frame_data(self, frame_data: Dict) -> Dict:
        """
        Process frame data and extract insights
        
        Args:
            frame_data: Frame analysis data from processor
            
        Returns:
            Analysis results and insights
        """
        if not frame_data:
            return {}
        
        # Store frame data
        frame_data['timestamp'] = time.time()
        self.frame_data.append(frame_data)
        
        # Update session stats
        self.current_session['frames_processed'] += 1
        
        # Analyze current frame
        analysis = self._analyze_current_frame(frame_data)
        
        # Detect events
        events = self._detect_events(frame_data)
        for event in events:
            self.events.append(event)
            self.current_session['events_detected'] += 1
        
        # Calculate performance metrics
        performance = self._calculate_performance_metrics()
        
        # Generate insights
        insights = self._generate_insights(analysis, events, performance)
        
        return {
            'analysis': analysis,
            'events': events,
            'performance': performance,
            'insights': insights,
            'session_stats': self.current_session.copy()
        }
    
    def _analyze_current_frame(self, frame_data: Dict) -> Dict:
        """
        Analyze current frame for immediate insights
        
        Args:
            frame_data: Current frame data
            
        Returns:
            Frame analysis results
        """
        analysis = {
            'crosshair_analysis': {},
            'enemy_analysis': {},
            'movement_analysis': {},
            'ui_analysis': {}
        }
        
        # Crosshair analysis
        if 'crosshair' in frame_data and frame_data['crosshair']:
            crosshair = frame_data['crosshair']
            analysis['crosshair_analysis'] = {
                'position': crosshair.position,
                'is_visible': crosshair.is_visible,
                'placement_quality': self._assess_crosshair_placement(crosshair, frame_data.get('enemies', [])),
                'stability': self._assess_crosshair_stability()
            }
        
        # Enemy analysis
        enemies = frame_data.get('enemies', [])
        if enemies:
            analysis['enemy_analysis'] = {
                'enemy_count': len(enemies),
                'closest_enemy': self._find_closest_enemy(enemies),
                'threat_level': self._assess_threat_level(enemies),
                'engagement_opportunity': self._assess_engagement_opportunity(enemies)
            }
        
        # Movement analysis
        movement = frame_data.get('movement', {})
        if movement:
            analysis['movement_analysis'] = {
                'is_moving': movement.get('is_moving', False),
                'movement_direction': movement.get('movement_direction', 'unknown'),
                'movement_magnitude': movement.get('movement_magnitude', 0.0),
                'movement_efficiency': self._assess_movement_efficiency(movement)
            }
        
        # UI analysis
        ui_elements = frame_data.get('ui_elements', [])
        if ui_elements:
            analysis['ui_analysis'] = {
                'ui_elements_detected': len(ui_elements),
                'health_status': self._assess_health_status(ui_elements),
                'ammo_status': self._assess_ammo_status(ui_elements)
            }
        
        return analysis
    
    def _detect_events(self, frame_data: Dict) -> List[GameEvent]:
        """
        Detect significant game events
        
        Args:
            frame_data: Current frame data
            
        Returns:
            List of detected events
        """
        events = []
        current_time = time.time()
        
        # Enemy detection event
        enemies = frame_data.get('enemies', [])
        if enemies and len(enemies) > 0:
            # Check if this is a new enemy detection
            if not self._has_recent_enemy_event(2.0):  # 2 second cooldown
                events.append(GameEvent(
                    event_type="enemy_detected",
                    timestamp=current_time,
                    confidence=0.8,
                    data={'enemy_count': len(enemies)},
                    position=enemies[0].center if enemies else None
                ))
        
        # Crosshair placement event
        crosshair = frame_data.get('crosshair')
        if crosshair and crosshair.is_visible:
            placement_quality = self._assess_crosshair_placement(crosshair, enemies)
            if placement_quality > 0.8:
                events.append(GameEvent(
                    event_type="good_crosshair_placement",
                    timestamp=current_time,
                    confidence=placement_quality,
                    data={'placement_quality': placement_quality},
                    position=crosshair.position
                ))
            elif placement_quality < 0.3:
                events.append(GameEvent(
                    event_type="poor_crosshair_placement",
                    timestamp=current_time,
                    confidence=1.0 - placement_quality,
                    data={'placement_quality': placement_quality},
                    position=crosshair.position
                ))
        
        # Movement events
        movement = frame_data.get('movement', {})
        if movement.get('is_moving', False):
            efficiency = self._assess_movement_efficiency(movement)
            if efficiency < 0.4:
                events.append(GameEvent(
                    event_type="inefficient_movement",
                    timestamp=current_time,
                    confidence=0.7,
                    data={'efficiency': efficiency},
                    position=None
                ))
        
        return events
    
    def _calculate_performance_metrics(self) -> PerformanceMetrics:
        """
        Calculate overall performance metrics
        
        Returns:
            Performance metrics object
        """
        if len(self.frame_data) < 10:
            return PerformanceMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
        # Calculate accuracy (based on crosshair placement)
        accuracy = self._calculate_accuracy()
        
        # Calculate reaction time
        reaction_time = self._calculate_reaction_time()
        
        # Calculate crosshair placement score
        crosshair_placement = self._calculate_crosshair_placement_score()
        
        # Calculate movement efficiency
        movement_efficiency = self._calculate_movement_efficiency()
        
        # Calculate game sense
        game_sense = self._calculate_game_sense()
        
        # Calculate overall score
        overall_score = (accuracy + crosshair_placement + movement_efficiency + game_sense) / 4
        
        metrics = PerformanceMetrics(
            accuracy=accuracy,
            reaction_time=reaction_time,
            crosshair_placement=crosshair_placement,
            movement_efficiency=movement_efficiency,
            game_sense=game_sense,
            overall_score=overall_score
        )
        
        # Store in history
        self.performance_history.append(metrics)
        
        return metrics
    
    def _generate_insights(self, analysis: Dict, events: List[GameEvent], performance: PerformanceMetrics) -> List[str]:
        """
        Generate coaching insights based on analysis
        
        Args:
            analysis: Frame analysis results
            events: Detected events
            performance: Performance metrics
            
        Returns:
            List of coaching insights
        """
        insights = []
        
        # Performance-based insights
        if performance.accuracy < 0.6:
            insights.append("Your accuracy needs improvement. Focus on crosshair placement and recoil control.")
        
        if performance.crosshair_placement < 0.5:
            insights.append("Work on keeping your crosshair at head level and pre-aiming common angles.")
        
        if performance.movement_efficiency < 0.4:
            insights.append("Your movement could be more efficient. Practice counter-strafing and positioning.")
        
        if performance.game_sense < 0.5:
            insights.append("Improve your game sense by learning common angles, timings, and team coordination.")
        
        # Event-based insights
        for event in events[-5:]:  # Last 5 events
            if event.event_type == "poor_crosshair_placement":
                insights.append("Your crosshair is not positioned optimally. Aim at head level.")
            elif event.event_type == "inefficient_movement":
                insights.append("You're moving inefficiently. Use counter-strafing and proper positioning.")
            elif event.event_type == "enemy_detected":
                insights.append("Enemy detected! Consider your positioning and team coordination.")
        
        # Analysis-based insights
        if analysis.get('enemy_analysis', {}).get('threat_level', 0) > 0.7:
            insights.append("High threat situation detected. Focus on positioning and team coordination.")
        
        if analysis.get('movement_analysis', {}).get('movement_magnitude', 0) > 5.0:
            insights.append("You're moving too much. Consider holding angles and being more patient.")
        
        return insights[:3]  # Limit to top 3 insights
    
    def _assess_crosshair_placement(self, crosshair, enemies: List) -> float:
        """Assess crosshair placement quality"""
        if not enemies:
            return 0.5  # Neutral score if no enemies
        
        # Find closest enemy
        closest_enemy = self._find_closest_enemy(enemies)
        if not closest_enemy:
            return 0.5
        
        # Calculate distance to enemy head level
        enemy_center = closest_enemy.center
        crosshair_pos = crosshair.position
        
        # Assume head level is roughly 1/3 from top of enemy bounding box
        head_level = enemy_center[1] - closest_enemy.bbox[3] // 3
        
        distance = abs(crosshair_pos[1] - head_level)
        max_distance = closest_enemy.bbox[3] // 2
        
        placement_score = max(0, 1 - (distance / max_distance))
        return min(1.0, placement_score)
    
    def _assess_crosshair_stability(self) -> float:
        """Assess crosshair stability over time"""
        if len(self.frame_data) < 5:
            return 0.5
        
        recent_positions = []
        for frame in list(self.frame_data)[-5:]:
            if frame.get('crosshair') and frame['crosshair'].is_visible:
                recent_positions.append(frame['crosshair'].position)
        
        if len(recent_positions) < 3:
            return 0.5
        
        # Calculate variance in position
        positions = np.array(recent_positions)
        variance = np.var(positions, axis=0).mean()
        
        # Convert to stability score (lower variance = higher stability)
        stability = max(0, 1 - (variance / 100))
        return min(1.0, stability)
    
    def _find_closest_enemy(self, enemies: List) -> Optional:
        """Find the closest enemy to screen center"""
        if not enemies:
            return None
        
        screen_center = (1920 // 2, 1080 // 2)  # Assuming 1920x1080
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = np.sqrt((enemy.center[0] - screen_center[0])**2 + 
                             (enemy.center[1] - screen_center[1])**2)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        
        return closest_enemy
    
    def _assess_threat_level(self, enemies: List) -> float:
        """Assess overall threat level from enemies"""
        if not enemies:
            return 0.0
        
        # Consider number of enemies and their proximity
        threat_score = len(enemies) * 0.2
        
        # Add proximity factor
        closest_enemy = self._find_closest_enemy(enemies)
        if closest_enemy:
            screen_center = (1920 // 2, 1080 // 2)
            distance = np.sqrt((closest_enemy.center[0] - screen_center[0])**2 + 
                             (closest_enemy.center[1] - screen_center[1])**2)
            proximity_factor = max(0, 1 - (distance / 1000))  # Closer = higher threat
            threat_score += proximity_factor * 0.5
        
        return min(1.0, threat_score)
    
    def _assess_engagement_opportunity(self, enemies: List) -> float:
        """Assess if this is a good engagement opportunity"""
        if not enemies:
            return 0.0
        
        # Consider enemy count (fewer enemies = better opportunity)
        enemy_factor = max(0, 1 - (len(enemies) - 1) * 0.3)
        
        # Consider positioning
        closest_enemy = self._find_closest_enemy(enemies)
        if closest_enemy:
            # Check if crosshair is close to enemy
            crosshair_pos = (1920 // 2, 1080 // 2)  # Assume center
            distance = np.sqrt((closest_enemy.center[0] - crosshair_pos[0])**2 + 
                             (closest_enemy.center[1] - crosshair_pos[1])**2)
            positioning_factor = max(0, 1 - (distance / 500))
            
            return (enemy_factor + positioning_factor) / 2
        
        return enemy_factor
    
    def _assess_movement_efficiency(self, movement: Dict) -> float:
        """Assess movement efficiency"""
        if not movement.get('is_moving', False):
            return 0.5  # Neutral for stationary
        
        magnitude = movement.get('movement_magnitude', 0)
        direction = movement.get('movement_direction', 'unknown')
        
        # Penalize excessive movement
        if magnitude > 10:
            return 0.3
        
        # Reward purposeful movement
        if direction != 'stationary' and magnitude > 1:
            return 0.7
        
        return 0.5
    
    def _assess_health_status(self, ui_elements: List) -> str:
        """Assess health status from UI elements"""
        # This would require more sophisticated UI analysis
        return "unknown"
    
    def _assess_ammo_status(self, ui_elements: List) -> str:
        """Assess ammo status from UI elements"""
        # This would require more sophisticated UI analysis
        return "unknown"
    
    def _has_recent_enemy_event(self, cooldown: float) -> bool:
        """Check if there was a recent enemy detection event"""
        current_time = time.time()
        for event in reversed(self.events):
            if event.event_type == "enemy_detected":
                if current_time - event.timestamp < cooldown:
                    return True
                break
        return False
    
    def _calculate_accuracy(self) -> float:
        """Calculate accuracy score"""
        if len(self.frame_data) < 10:
            return 0.5
        
        # Calculate based on crosshair placement quality
        placement_scores = []
        for frame in list(self.frame_data)[-30:]:  # Last 30 frames
            if frame.get('crosshair') and frame.get('enemies'):
                score = self._assess_crosshair_placement(frame['crosshair'], frame['enemies'])
                placement_scores.append(score)
        
        return np.mean(placement_scores) if placement_scores else 0.5
    
    def _calculate_reaction_time(self) -> float:
        """Calculate average reaction time"""
        # This would require more sophisticated event tracking
        return 0.3  # Placeholder
    
    def _calculate_crosshair_placement_score(self) -> float:
        """Calculate crosshair placement score"""
        if len(self.frame_data) < 10:
            return 0.5
        
        placement_scores = []
        for frame in list(self.frame_data)[-30:]:
            if frame.get('crosshair'):
                stability = self._assess_crosshair_stability()
                placement_scores.append(stability)
        
        return np.mean(placement_scores) if placement_scores else 0.5
    
    def _calculate_movement_efficiency(self) -> float:
        """Calculate movement efficiency score"""
        if len(self.frame_data) < 10:
            return 0.5
        
        efficiency_scores = []
        for frame in list(self.frame_data)[-30:]:
            if frame.get('movement'):
                efficiency = self._assess_movement_efficiency(frame['movement'])
                efficiency_scores.append(efficiency)
        
        return np.mean(efficiency_scores) if efficiency_scores else 0.5
    
    def _calculate_game_sense(self) -> float:
        """Calculate game sense score"""
        # This is a complex metric that would require more sophisticated analysis
        # For now, return a placeholder based on event detection
        if len(self.events) < 5:
            return 0.5
        
        # Count positive events vs negative events
        positive_events = sum(1 for event in self.events if event.event_type in ["good_crosshair_placement"])
        negative_events = sum(1 for event in self.events if event.event_type in ["poor_crosshair_placement", "inefficient_movement"])
        
        total_events = positive_events + negative_events
        if total_events == 0:
            return 0.5
        
        return positive_events / total_events
    
    def get_session_summary(self) -> Dict:
        """Get summary of current session"""
        return {
            'session_duration': time.time() - self.start_time,
            'frames_processed': self.current_session['frames_processed'],
            'events_detected': self.current_session['events_detected'],
            'performance_history': list(self.performance_history),
            'current_performance': self.performance_history[-1] if self.performance_history else None
        }