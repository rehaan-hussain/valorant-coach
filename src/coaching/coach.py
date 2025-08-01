"""
Main coaching system for Valorant players
"""

import time
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class CoachingTip:
    """Represents a coaching tip"""
    tip_id: str
    category: str
    priority: int  # 1-5, 5 being highest
    message: str
    timestamp: float
    context: Dict
    actionable: bool = True

@dataclass
class PlayerProfile:
    """Player profile and skill assessment"""
    skill_level: str  # "beginner", "intermediate", "advanced"
    primary_role: str  # "duelist", "sentinel", "initiator", "controller"
    strengths: List[str]
    weaknesses: List[str]
    goals: List[str]
    playtime_hours: int

class Coach:
    """
    Main coaching system that provides personalized advice
    """
    
    def __init__(self, player_profile: Optional[PlayerProfile] = None):
        """
        Initialize coach
        
        Args:
            player_profile: Player profile for personalized coaching
        """
        self.player_profile = player_profile or self._create_default_profile()
        
        # Coaching state
        self.tip_history = deque(maxlen=100)
        self.session_tips = deque(maxlen=50)
        self.last_tip_time = 0
        self.tip_cooldown = 5.0  # Minimum seconds between tips
        
        # Performance tracking
        self.performance_history = deque(maxlen=100)
        self.improvement_areas = []
        
        # Tip categories and priorities
        self.tip_categories = {
            'crosshair_placement': 5,
            'movement': 4,
            'positioning': 4,
            'game_sense': 3,
            'mechanics': 3,
            'teamwork': 2,
            'economy': 2
        }
        
        logger.info("Coach initialized")
    
    def process_analysis(self, analysis_data: Dict) -> List[CoachingTip]:
        """
        Process analysis data and generate coaching tips
        
        Args:
            analysis_data: Analysis results from game analyzer
            
        Returns:
            List of coaching tips
        """
        if not analysis_data:
            return []
        
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_tip_time < self.tip_cooldown:
            return []
        
        tips = []
        
        # Generate tips based on analysis
        performance = analysis_data.get('performance')
        if performance:
            tips.extend(self._generate_performance_tips(performance))
        
        events = analysis_data.get('events', [])
        if events:
            tips.extend(self._generate_event_tips(events))
        
        insights = analysis_data.get('insights', [])
        if insights:
            tips.extend(self._generate_insight_tips(insights))
        
        # Filter and prioritize tips
        filtered_tips = self._filter_tips(tips)
        
        # Update state
        for tip in filtered_tips:
            self.tip_history.append(tip)
            self.session_tips.append(tip)
        
        if filtered_tips:
            self.last_tip_time = current_time
        
        return filtered_tips[:3]  # Return top 3 tips
    
    def get_personalized_advice(self, skill_area: str) -> List[str]:
        """
        Get personalized advice for specific skill areas
        
        Args:
            skill_area: Area to focus on
            
        Returns:
            List of personalized advice
        """
        advice = []
        
        if skill_area == "crosshair_placement":
            advice = self._get_crosshair_advice()
        elif skill_area == "movement":
            advice = self._get_movement_advice()
        elif skill_area == "positioning":
            advice = self._get_positioning_advice()
        elif skill_area == "game_sense":
            advice = self._get_game_sense_advice()
        elif skill_area == "mechanics":
            advice = self._get_mechanics_advice()
        else:
            advice = ["Focus on improving your overall gameplay fundamentals."]
        
        return advice
    
    def generate_training_plan(self, focus_areas: List[str] = None) -> Dict:
        """
        Generate a personalized training plan
        
        Args:
            focus_areas: Specific areas to focus on
            
        Returns:
            Training plan dictionary
        """
        if not focus_areas:
            focus_areas = self._identify_weakest_areas()
        
        training_plan = {
            'focus_areas': focus_areas,
            'exercises': {},
            'duration': '30 minutes',
            'frequency': 'daily',
            'goals': []
        }
        
        for area in focus_areas:
            training_plan['exercises'][area] = self._get_exercises_for_area(area)
            training_plan['goals'].append(self._get_goal_for_area(area))
        
        return training_plan
    
    def update_player_profile(self, new_data: Dict):
        """
        Update player profile with new information
        
        Args:
            new_data: New player data
        """
        if 'skill_level' in new_data:
            self.player_profile.skill_level = new_data['skill_level']
        
        if 'primary_role' in new_data:
            self.player_profile.primary_role = new_data['primary_role']
        
        if 'strengths' in new_data:
            self.player_profile.strengths = new_data['strengths']
        
        if 'weaknesses' in new_data:
            self.player_profile.weaknesses = new_data['weaknesses']
        
        if 'goals' in new_data:
            self.player_profile.goals = new_data['goals']
        
        logger.info("Player profile updated")
    
    def _generate_performance_tips(self, performance) -> List[CoachingTip]:
        """Generate tips based on performance metrics"""
        tips = []
        current_time = time.time()
        
        # Accuracy tips
        if performance.accuracy < 0.6:
            tips.append(CoachingTip(
                tip_id=f"accuracy_{current_time}",
                category="mechanics",
                priority=5,
                message="Your accuracy needs improvement. Practice in the Range with different weapons and focus on recoil control.",
                timestamp=current_time,
                context={'accuracy': performance.accuracy}
            ))
        
        # Crosshair placement tips
        if performance.crosshair_placement < 0.5:
            tips.append(CoachingTip(
                tip_id=f"crosshair_{current_time}",
                category="crosshair_placement",
                priority=5,
                message="Keep your crosshair at head level and pre-aim common angles. This will improve your reaction time and accuracy.",
                timestamp=current_time,
                context={'crosshair_placement': performance.crosshair_placement}
            ))
        
        # Movement tips
        if performance.movement_efficiency < 0.4:
            tips.append(CoachingTip(
                tip_id=f"movement_{current_time}",
                category="movement",
                priority=4,
                message="Practice counter-strafing and efficient movement. Don't move while shooting unless necessary.",
                timestamp=current_time,
                context={'movement_efficiency': performance.movement_efficiency}
            ))
        
        # Game sense tips
        if performance.game_sense < 0.5:
            tips.append(CoachingTip(
                tip_id=f"gamesense_{current_time}",
                category="game_sense",
                priority=3,
                message="Improve your game sense by learning common angles, timings, and team coordination patterns.",
                timestamp=current_time,
                context={'game_sense': performance.game_sense}
            ))
        
        return tips
    
    def _generate_event_tips(self, events: List) -> List[CoachingTip]:
        """Generate tips based on detected events"""
        tips = []
        current_time = time.time()
        
        for event in events[-3:]:  # Last 3 events
            if event.event_type == "poor_crosshair_placement":
                tips.append(CoachingTip(
                    tip_id=f"event_crosshair_{current_time}",
                    category="crosshair_placement",
                    priority=4,
                    message="Your crosshair placement was poor. Aim at head level and pre-aim angles.",
                    timestamp=current_time,
                    context={'event_type': event.event_type}
                ))
            
            elif event.event_type == "inefficient_movement":
                tips.append(CoachingTip(
                    tip_id=f"event_movement_{current_time}",
                    category="movement",
                    priority=3,
                    message="Your movement was inefficient. Use counter-strafing and proper positioning.",
                    timestamp=current_time,
                    context={'event_type': event.event_type}
                ))
            
            elif event.event_type == "enemy_detected":
                tips.append(CoachingTip(
                    tip_id=f"event_enemy_{current_time}",
                    category="game_sense",
                    priority=3,
                    message="Enemy detected! Consider your positioning and communicate with your team.",
                    timestamp=current_time,
                    context={'event_type': event.event_type}
                ))
        
        return tips
    
    def _generate_insight_tips(self, insights: List[str]) -> List[CoachingTip]:
        """Generate tips based on analysis insights"""
        tips = []
        current_time = time.time()
        
        for i, insight in enumerate(insights[:2]):  # Top 2 insights
            # Determine category and priority based on insight content
            category = "general"
            priority = 3
            
            if "crosshair" in insight.lower():
                category = "crosshair_placement"
                priority = 4
            elif "movement" in insight.lower():
                category = "movement"
                priority = 4
            elif "positioning" in insight.lower():
                category = "positioning"
                priority = 4
            elif "accuracy" in insight.lower():
                category = "mechanics"
                priority = 5
            
            tips.append(CoachingTip(
                tip_id=f"insight_{current_time}_{i}",
                category=category,
                priority=priority,
                message=insight,
                timestamp=current_time,
                context={'insight_index': i}
            ))
        
        return tips
    
    def _filter_tips(self, tips: List[CoachingTip]) -> List[CoachingTip]:
        """Filter and prioritize tips"""
        if not tips:
            return []
        
        # Sort by priority (highest first)
        tips.sort(key=lambda x: x.priority, reverse=True)
        
        # Remove duplicates (same category)
        filtered_tips = []
        seen_categories = set()
        
        for tip in tips:
            if tip.category not in seen_categories:
                filtered_tips.append(tip)
                seen_categories.add(tip.category)
        
        return filtered_tips
    
    def _get_crosshair_advice(self) -> List[str]:
        """Get personalized crosshair placement advice"""
        advice = [
            "Always keep your crosshair at head level",
            "Pre-aim common angles where enemies might appear",
            "Practice flicking to different head heights",
            "Use the Range to practice crosshair placement",
            "Don't look at the ground - keep your crosshair up"
        ]
        
        if self.player_profile.skill_level == "beginner":
            advice.extend([
                "Start with a simple crosshair and practice in the Range",
                "Focus on keeping your crosshair steady while moving"
            ])
        
        return advice
    
    def _get_movement_advice(self) -> List[str]:
        """Get personalized movement advice"""
        advice = [
            "Learn counter-strafing to stop quickly",
            "Don't move while shooting unless necessary",
            "Use movement to peek angles efficiently",
            "Practice strafe shooting in the Range",
            "Use sound cues to time your movements"
        ]
        
        if self.player_profile.primary_role == "duelist":
            advice.extend([
                "As a duelist, focus on aggressive movement and entry fragging",
                "Use abilities to create movement opportunities"
            ])
        
        return advice
    
    def _get_positioning_advice(self) -> List[str]:
        """Get personalized positioning advice"""
        advice = [
            "Always have cover nearby",
            "Don't expose yourself to multiple angles",
            "Use off-angles to catch enemies off guard",
            "Position yourself to help your team",
            "Learn common positions for each map"
        ]
        
        return advice
    
    def _get_game_sense_advice(self) -> List[str]:
        """Get personalized game sense advice"""
        advice = [
            "Learn common timings and rotations",
            "Communicate with your team effectively",
            "Understand economy and buy rounds",
            "Learn from your mistakes and adapt",
            "Watch professional players to learn strategies"
        ]
        
        return advice
    
    def _get_mechanics_advice(self) -> List[str]:
        """Get personalized mechanics advice"""
        advice = [
            "Practice recoil control with different weapons",
            "Learn spray patterns for your main weapons",
            "Practice flicking and tracking in the Range",
            "Work on your reaction time",
            "Use aim training maps to improve accuracy"
        ]
        
        return advice
    
    def _identify_weakest_areas(self) -> List[str]:
        """Identify player's weakest areas based on profile and history"""
        if not self.player_profile.weaknesses:
            return ["crosshair_placement", "movement"]
        
        # Map weaknesses to training areas
        weakness_mapping = {
            "aim": "mechanics",
            "positioning": "positioning",
            "game sense": "game_sense",
            "movement": "movement",
            "crosshair placement": "crosshair_placement"
        }
        
        areas = []
        for weakness in self.player_profile.weaknesses:
            if weakness.lower() in weakness_mapping:
                areas.append(weakness_mapping[weakness.lower()])
        
        return areas if areas else ["crosshair_placement", "movement"]
    
    def _get_exercises_for_area(self, area: str) -> List[str]:
        """Get specific exercises for a training area"""
        exercises = {
            "crosshair_placement": [
                "Practice in the Range with different weapons",
                "Use aim training maps focusing on head level",
                "Practice pre-aiming common angles",
                "Work on crosshair placement while moving"
            ],
            "movement": [
                "Practice counter-strafing in the Range",
                "Work on strafe shooting",
                "Practice movement while maintaining accuracy",
                "Learn efficient peeking techniques"
            ],
            "positioning": [
                "Study common positions on each map",
                "Practice holding angles",
                "Work on off-angle positioning",
                "Learn rotation timings"
            ],
            "game_sense": [
                "Watch professional matches",
                "Review your own gameplay",
                "Learn economy management",
                "Practice communication with team"
            ],
            "mechanics": [
                "Practice recoil control",
                "Work on flicking and tracking",
                "Use aim training maps",
                "Practice with different weapons"
            ]
        }
        
        return exercises.get(area, ["General practice and improvement"])
    
    def _get_goal_for_area(self, area: str) -> str:
        """Get a specific goal for a training area"""
        goals = {
            "crosshair_placement": "Improve crosshair placement accuracy by 20%",
            "movement": "Master counter-strafing and efficient movement",
            "positioning": "Learn optimal positions for each map",
            "game_sense": "Improve decision making and team coordination",
            "mechanics": "Improve overall accuracy and recoil control"
        }
        
        return goals.get(area, "Improve overall performance")
    
    def _create_default_profile(self) -> PlayerProfile:
        """Create a default player profile"""
        return PlayerProfile(
            skill_level="beginner",
            primary_role="duelist",
            strengths=["enthusiasm", "willingness to learn"],
            weaknesses=["aim", "positioning", "game sense"],
            goals=["improve overall gameplay", "reach higher rank"],
            playtime_hours=0
        )
    
    def get_coaching_stats(self) -> Dict:
        """Get coaching statistics"""
        return {
            'total_tips_given': len(self.tip_history),
            'session_tips': len(self.session_tips),
            'player_profile': self.player_profile,
            'tip_categories': self.tip_categories
        }