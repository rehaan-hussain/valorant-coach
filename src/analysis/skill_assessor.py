"""
Skill assessment module for evaluating player performance
"""

import numpy as np
from typing import Dict, List, Tuple
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SkillAssessment:
    """Represents a skill assessment"""
    skill_name: str
    score: float
    confidence: float
    improvement_needed: bool
    recommendations: List[str]

class SkillAssessor:
    """
    Assesses player skills based on gameplay data
    """
    
    def __init__(self):
        """Initialize skill assessor"""
        self.skill_weights = {
            'aim': 0.25,
            'crosshair_placement': 0.20,
            'movement': 0.15,
            'positioning': 0.15,
            'game_sense': 0.15,
            'reaction_time': 0.10
        }
        
        self.skill_thresholds = {
            'beginner': 0.3,
            'intermediate': 0.6,
            'advanced': 0.8
        }
        
        logger.info("Skill assessor initialized")
    
    def assess_skills(self, performance_data: Dict) -> Dict[str, SkillAssessment]:
        """
        Assess all player skills
        
        Args:
            performance_data: Performance metrics and analysis data
            
        Returns:
            Dictionary of skill assessments
        """
        assessments = {}
        
        # Assess individual skills
        assessments['aim'] = self._assess_aim(performance_data)
        assessments['crosshair_placement'] = self._assess_crosshair_placement(performance_data)
        assessments['movement'] = self._assess_movement(performance_data)
        assessments['positioning'] = self._assess_positioning(performance_data)
        assessments['game_sense'] = self._assess_game_sense(performance_data)
        assessments['reaction_time'] = self._assess_reaction_time(performance_data)
        
        return assessments
    
    def get_overall_skill_level(self, assessments: Dict[str, SkillAssessment]) -> str:
        """
        Determine overall skill level
        
        Args:
            assessments: Skill assessments
            
        Returns:
            Skill level string
        """
        if not assessments:
            return "beginner"
        
        # Calculate weighted average
        total_score = 0
        total_weight = 0
        
        for skill_name, assessment in assessments.items():
            weight = self.skill_weights.get(skill_name, 0.1)
            total_score += assessment.score * weight
            total_weight += weight
        
        if total_weight == 0:
            return "beginner"
        
        overall_score = total_score / total_weight
        
        # Determine skill level
        if overall_score >= self.skill_thresholds['advanced']:
            return "advanced"
        elif overall_score >= self.skill_thresholds['intermediate']:
            return "intermediate"
        else:
            return "beginner"
    
    def _assess_aim(self, performance_data: Dict) -> SkillAssessment:
        """Assess aim skill"""
        accuracy = performance_data.get('accuracy', 0.5)
        
        # Calculate aim score based on accuracy
        aim_score = min(1.0, accuracy * 1.5)  # Scale accuracy to aim score
        
        recommendations = []
        if aim_score < 0.4:
            recommendations.extend([
                "Practice in the Range with different weapons",
                "Focus on recoil control",
                "Use aim training maps"
            ])
        elif aim_score < 0.7:
            recommendations.extend([
                "Work on flicking accuracy",
                "Practice tracking moving targets",
                "Improve spray control"
            ])
        
        return SkillAssessment(
            skill_name="aim",
            score=aim_score,
            confidence=0.8,
            improvement_needed=aim_score < 0.6,
            recommendations=recommendations
        )
    
    def _assess_crosshair_placement(self, performance_data: Dict) -> SkillAssessment:
        """Assess crosshair placement skill"""
        crosshair_score = performance_data.get('crosshair_placement', 0.5)
        
        recommendations = []
        if crosshair_score < 0.4:
            recommendations.extend([
                "Keep crosshair at head level",
                "Pre-aim common angles",
                "Practice crosshair placement in the Range"
            ])
        elif crosshair_score < 0.7:
            recommendations.extend([
                "Improve crosshair stability",
                "Work on pre-aiming multiple angles",
                "Practice crosshair placement while moving"
            ])
        
        return SkillAssessment(
            skill_name="crosshair_placement",
            score=crosshair_score,
            confidence=0.9,
            improvement_needed=crosshair_score < 0.6,
            recommendations=recommendations
        )
    
    def _assess_movement(self, performance_data: Dict) -> SkillAssessment:
        """Assess movement skill"""
        movement_score = performance_data.get('movement_efficiency', 0.5)
        
        recommendations = []
        if movement_score < 0.4:
            recommendations.extend([
                "Learn counter-strafing",
                "Practice efficient movement patterns",
                "Don't move while shooting"
            ])
        elif movement_score < 0.7:
            recommendations.extend([
                "Improve strafe shooting",
                "Work on movement timing",
                "Practice movement with abilities"
            ])
        
        return SkillAssessment(
            skill_name="movement",
            score=movement_score,
            confidence=0.7,
            improvement_needed=movement_score < 0.5,
            recommendations=recommendations
        )
    
    def _assess_positioning(self, performance_data: Dict) -> SkillAssessment:
        """Assess positioning skill"""
        # This would require more sophisticated analysis
        # For now, use a placeholder based on other metrics
        game_sense = performance_data.get('game_sense', 0.5)
        positioning_score = game_sense * 0.8  # Rough estimate
        
        recommendations = []
        if positioning_score < 0.4:
            recommendations.extend([
                "Learn common positions on each map",
                "Always have cover nearby",
                "Don't expose yourself to multiple angles"
            ])
        elif positioning_score < 0.7:
            recommendations.extend([
                "Work on off-angle positioning",
                "Improve rotation timing",
                "Learn team positioning"
            ])
        
        return SkillAssessment(
            skill_name="positioning",
            score=positioning_score,
            confidence=0.6,
            improvement_needed=positioning_score < 0.5,
            recommendations=recommendations
        )
    
    def _assess_game_sense(self, performance_data: Dict) -> SkillAssessment:
        """Assess game sense skill"""
        game_sense_score = performance_data.get('game_sense', 0.5)
        
        recommendations = []
        if game_sense_score < 0.4:
            recommendations.extend([
                "Watch professional matches",
                "Learn common timings and rotations",
                "Improve communication with team"
            ])
        elif game_sense_score < 0.7:
            recommendations.extend([
                "Study opponent patterns",
                "Improve decision making",
                "Learn economy management"
            ])
        
        return SkillAssessment(
            skill_name="game_sense",
            score=game_sense_score,
            confidence=0.7,
            improvement_needed=game_sense_score < 0.5,
            recommendations=recommendations
        )
    
    def _assess_reaction_time(self, performance_data: Dict) -> SkillAssessment:
        """Assess reaction time skill"""
        reaction_time = performance_data.get('reaction_time', 0.3)
        
        # Convert reaction time to score (lower is better)
        reaction_score = max(0, 1 - (reaction_time - 0.2) / 0.3)
        
        recommendations = []
        if reaction_score < 0.4:
            recommendations.extend([
                "Practice reaction time exercises",
                "Improve focus and concentration",
                "Work on anticipation"
            ])
        elif reaction_score < 0.7:
            recommendations.extend([
                "Practice flicking to targets",
                "Work on quick decision making",
                "Improve visual processing"
            ])
        
        return SkillAssessment(
            skill_name="reaction_time",
            score=reaction_score,
            confidence=0.5,  # Lower confidence due to limited data
            improvement_needed=reaction_score < 0.6,
            recommendations=recommendations
        )
    
    def get_skill_improvement_plan(self, assessments: Dict[str, SkillAssessment]) -> Dict:
        """
        Generate improvement plan based on skill assessments
        
        Args:
            assessments: Skill assessments
            
        Returns:
            Improvement plan dictionary
        """
        plan = {
            'priority_skills': [],
            'exercises': {},
            'estimated_improvement_time': '2-4 weeks',
            'goals': []
        }
        
        # Identify priority skills (those needing improvement)
        priority_skills = []
        for skill_name, assessment in assessments.items():
            if assessment.improvement_needed:
                priority_skills.append((skill_name, assessment.score))
        
        # Sort by score (lowest first)
        priority_skills.sort(key=lambda x: x[1])
        plan['priority_skills'] = [skill[0] for skill in priority_skills[:3]]
        
        # Generate exercises for priority skills
        for skill_name in plan['priority_skills']:
            assessment = assessments[skill_name]
            plan['exercises'][skill_name] = assessment.recommendations
        
        # Generate goals
        for skill_name in plan['priority_skills']:
            current_score = assessments[skill_name].score
            target_score = min(1.0, current_score + 0.2)  # Aim for 20% improvement
            plan['goals'].append(f"Improve {skill_name} from {current_score:.1%} to {target_score:.1%}")
        
        return plan