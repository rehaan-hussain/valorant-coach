"""
Frame processing and game element detection
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class GameElement:
    """Represents a detected game element"""
    type: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    center: Tuple[int, int]
    color: Optional[Tuple[int, int, int]] = None

@dataclass
class CrosshairInfo:
    """Crosshair position and state"""
    position: Tuple[int, int]
    is_visible: bool
    color: Tuple[int, int, int]

class FrameProcessor:
    """
    Processes captured frames to detect Valorant game elements
    """
    
    def __init__(self):
        """Initialize frame processor"""
        self.frame_history = []
        self.max_history = 30  # Keep last 30 frames
        
        # Detection thresholds
        self.crosshair_threshold = 0.8
        self.enemy_threshold = 0.6
        self.ui_threshold = 0.7
        
        # Color ranges for detection
        self.crosshair_colors = [
            ([0, 0, 200], [50, 50, 255]),  # Red
            ([200, 0, 0], [255, 50, 50]),  # Blue
            ([0, 200, 0], [50, 255, 50]),  # Green
        ]
        
        logger.info("Frame processor initialized")
    
    def process_frame(self, frame: np.ndarray) -> Dict:
        """
        Process a single frame and detect game elements
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            Dictionary containing detected elements and analysis
        """
        if frame is None:
            return {}
        
        # Add to history
        self.frame_history.append(frame.copy())
        if len(self.frame_history) > self.max_history:
            self.frame_history.pop(0)
        
        # Detect elements
        crosshair = self._detect_crosshair(frame)
        enemies = self._detect_enemies(frame)
        ui_elements = self._detect_ui_elements(frame)
        movement = self._analyze_movement()
        
        return {
            'crosshair': crosshair,
            'enemies': enemies,
            'ui_elements': ui_elements,
            'movement': movement,
            'timestamp': len(self.frame_history)
        }
    
    def _detect_crosshair(self, frame: np.ndarray) -> Optional[CrosshairInfo]:
        """
        Detect crosshair position and state
        
        Args:
            frame: Input frame
            
        Returns:
            CrosshairInfo object or None if not detected
        """
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Get frame center
            height, width = frame.shape[:2]
            center_x, center_y = width // 2, height // 2
            
            # Define crosshair search region (center area)
            search_radius = 50
            x1 = max(0, center_x - search_radius)
            y1 = max(0, center_y - search_radius)
            x2 = min(width, center_x + search_radius)
            y2 = min(height, center_y + search_radius)
            
            center_region = frame[y1:y2, x1:x2]
            
            # Look for crosshair patterns
            for color_range in self.crosshair_colors:
                lower, upper = color_range
                mask = cv2.inRange(center_region, np.array(lower), np.array(upper))
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 10 and area < 500:  # Reasonable crosshair size
                        # Get contour center
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"]) + x1
                            cy = int(M["m01"] / M["m00"]) + y1
                            
                            # Check if it's near screen center
                            distance = np.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                            if distance < search_radius:
                                return CrosshairInfo(
                                    position=(cx, cy),
                                    is_visible=True,
                                    color=tuple(color_range[0])
                                )
            
            # If no crosshair detected, return center position
            return CrosshairInfo(
                position=(center_x, center_y),
                is_visible=False,
                color=(255, 255, 255)
            )
            
        except Exception as e:
            logger.error(f"Error detecting crosshair: {e}")
            return None
    
    def _detect_enemies(self, frame: np.ndarray) -> List[GameElement]:
        """
        Detect enemy players in the frame
        
        Args:
            frame: Input frame
            
        Returns:
            List of detected enemy elements
        """
        enemies = []
        
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Enemy color detection (red team)
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            enemy_mask = mask1 + mask2
            
            # Find contours
            contours, _ = cv2.findContours(enemy_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Minimum enemy size
                    x, y, w, h = cv2.boundingRect(contour)
                    center = (x + w//2, y + h//2)
                    
                    # Calculate confidence based on size and position
                    confidence = min(1.0, area / 1000)
                    
                    enemies.append(GameElement(
                        type="enemy",
                        confidence=confidence,
                        bbox=(x, y, w, h),
                        center=center,
                        color=(0, 0, 255)
                    ))
            
        except Exception as e:
            logger.error(f"Error detecting enemies: {e}")
        
        return enemies
    
    def _detect_ui_elements(self, frame: np.ndarray) -> List[GameElement]:
        """
        Detect UI elements like health, ammo, minimap
        
        Args:
            frame: Input frame
            
        Returns:
            List of detected UI elements
        """
        ui_elements = []
        
        try:
            # Detect health bar (green)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_green = np.array([40, 100, 100])
            upper_green = np.array([80, 255, 255])
            health_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Detect ammo counter (white text)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, ammo_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            # Find UI regions (bottom corners)
            height, width = frame.shape[:2]
            
            # Bottom left (health/armor)
            bottom_left = frame[height-100:height, 0:200]
            if np.mean(bottom_left) > 50:
                ui_elements.append(GameElement(
                    type="health_ui",
                    confidence=0.8,
                    bbox=(0, height-100, 200, 100),
                    center=(100, height-50)
                ))
            
            # Bottom right (ammo/minimap)
            bottom_right = frame[height-100:height, width-200:width]
            if np.mean(bottom_right) > 50:
                ui_elements.append(GameElement(
                    type="ammo_ui",
                    confidence=0.8,
                    bbox=(width-200, height-100, 200, 100),
                    center=(width-100, height-50)
                ))
            
        except Exception as e:
            logger.error(f"Error detecting UI elements: {e}")
        
        return ui_elements
    
    def _analyze_movement(self) -> Dict:
        """
        Analyze movement patterns from frame history
        
        Returns:
            Movement analysis data
        """
        if len(self.frame_history) < 2:
            return {}
        
        try:
            # Compare last two frames
            prev_frame = cv2.cvtColor(self.frame_history[-2], cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(self.frame_history[-1], cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow
            flow = cv2.calcOpticalFlowFarneback(
                prev_frame, curr_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            
            # Calculate movement magnitude
            magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
            mean_movement = np.mean(magnitude)
            
            return {
                'movement_magnitude': float(mean_movement),
                'is_moving': mean_movement > 1.0,
                'movement_direction': self._get_movement_direction(flow)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing movement: {e}")
            return {}
    
    def _get_movement_direction(self, flow: np.ndarray) -> str:
        """
        Determine movement direction from optical flow
        
        Args:
            flow: Optical flow array
            
        Returns:
            Movement direction string
        """
        try:
            # Calculate average flow in different regions
            height, width = flow.shape[:2]
            
            # Split frame into quadrants
            mid_h, mid_w = height // 2, width // 2
            
            # Calculate average flow in each quadrant
            top_left = np.mean(flow[:mid_h, :mid_w], axis=(0, 1))
            top_right = np.mean(flow[:mid_h, mid_w:], axis=(0, 1))
            bottom_left = np.mean(flow[mid_h:, :mid_w], axis=(0, 1))
            bottom_right = np.mean(flow[mid_h:, mid_w:], axis=(0, 1))
            
            # Determine dominant direction
            directions = {
                'up': top_left[1] + top_right[1],
                'down': bottom_left[1] + bottom_right[1],
                'left': top_left[0] + bottom_left[0],
                'right': top_right[0] + bottom_right[0]
            }
            
            max_direction = max(directions, key=directions.get)
            return max_direction if abs(directions[max_direction]) > 0.5 else 'stationary'
            
        except Exception as e:
            logger.error(f"Error getting movement direction: {e}")
            return 'unknown'
    
    def get_frame_stats(self) -> Dict:
        """
        Get processing statistics
        
        Returns:
            Dictionary with processing statistics
        """
        return {
            'frames_processed': len(self.frame_history),
            'max_history': self.max_history,
            'detection_thresholds': {
                'crosshair': self.crosshair_threshold,
                'enemy': self.enemy_threshold,
                'ui': self.ui_threshold
            }
        }