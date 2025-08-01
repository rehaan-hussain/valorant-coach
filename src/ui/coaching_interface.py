"""
Coaching interface module for displaying coaching tips
"""

import logging

logger = logging.getLogger(__name__)

class CoachingInterface:
    """Interface for displaying coaching tips and feedback"""
    
    def __init__(self):
        """Initialize coaching interface"""
        logger.info("Coaching interface initialized")
    
    def display_tips(self, tips: list):
        """Display coaching tips"""
        # This is a placeholder - actual implementation would be in the Streamlit app
        pass