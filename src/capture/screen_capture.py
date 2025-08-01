"""
Screen capture module for Valorant gameplay
"""

import cv2
import numpy as np
import mss
import time
import threading
from typing import Optional, Callable, Tuple
import logging

logger = logging.getLogger(__name__)

class ScreenCapture:
    """
    Handles real-time screen capture for Valorant gameplay analysis
    """
    
    def __init__(self, monitor_id: int = 1, fps: int = 30):
        """
        Initialize screen capture
        
        Args:
            monitor_id: Monitor to capture (1 = primary monitor)
            fps: Target frames per second
        """
        self.monitor_id = monitor_id
        self.target_fps = fps
        self.frame_interval = 1.0 / fps
        
        # Initialize screen capture
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_id]
        
        # Capture state
        self.is_capturing = False
        self.capture_thread = None
        self.frame_callback = None
        
        # Performance tracking
        self.frame_count = 0
        self.start_time = None
        self.actual_fps = 0
        
        logger.info(f"Screen capture initialized for monitor {monitor_id}")
    
    def start_capture(self, callback: Optional[Callable] = None):
        """
        Start capturing frames
        
        Args:
            callback: Function to call with each captured frame
        """
        if self.is_capturing:
            logger.warning("Capture already running")
            return
        
        self.frame_callback = callback
        self.is_capturing = True
        self.frame_count = 0
        self.start_time = time.time()
        
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        logger.info("Screen capture started")
    
    def stop_capture(self):
        """Stop capturing frames"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.actual_fps = self.frame_count / elapsed if elapsed > 0 else 0
            logger.info(f"Capture stopped. FPS: {self.actual_fps:.2f}")
    
    def _capture_loop(self):
        """Main capture loop"""
        last_frame_time = time.time()
        
        while self.is_capturing:
            current_time = time.time()
            
            # Maintain target FPS
            if current_time - last_frame_time >= self.frame_interval:
                try:
                    # Capture screen
                    screenshot = self.sct.grab(self.monitor)
                    frame = np.array(screenshot)
                    
                    # Convert from BGRA to BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    
                    self.frame_count += 1
                    last_frame_time = current_time
                    
                    # Call callback if provided
                    if self.frame_callback:
                        self.frame_callback(frame)
                        
                except Exception as e:
                    logger.error(f"Error capturing frame: {e}")
                    time.sleep(0.01)  # Brief pause on error
            else:
                time.sleep(0.001)  # Small sleep to prevent busy waiting
    
    def capture_single_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame
        
        Returns:
            Captured frame as numpy array or None if failed
        """
        try:
            screenshot = self.sct.grab(self.monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame
        except Exception as e:
            logger.error(f"Error capturing single frame: {e}")
            return None
    
    def get_capture_stats(self) -> dict:
        """
        Get capture statistics
        
        Returns:
            Dictionary with capture statistics
        """
        return {
            'is_capturing': self.is_capturing,
            'frame_count': self.frame_count,
            'actual_fps': self.actual_fps,
            'target_fps': self.target_fps,
            'monitor': self.monitor
        }
    
    def set_region(self, x: int, y: int, width: int, height: int):
        """
        Set capture region (useful for capturing specific game window)
        
        Args:
            x, y: Top-left corner coordinates
            width, height: Region dimensions
        """
        self.monitor = {
            'top': y,
            'left': x,
            'width': width,
            'height': height
        }
        logger.info(f"Capture region set to {width}x{height} at ({x}, {y})")
    
    def __del__(self):
        """Cleanup on destruction"""
        self.stop_capture()
        if hasattr(self, 'sct'):
            self.sct.close()