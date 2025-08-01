"""
Configuration management for Valorant AI Coach
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file or "config/settings.json"
        self.config = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "capture": {
                "default_fps": 30,
                "default_monitor": 1,
                "max_frame_history": 1800
            },
            "analysis": {
                "session_duration": 300,
                "accuracy_threshold": 0.7,
                "reaction_threshold": 0.3,
                "movement_threshold": 0.5
            },
            "coaching": {
                "tip_cooldown": 5.0,
                "max_tips_per_session": 50,
                "tip_priority_levels": 5
            },
            "ui": {
                "default_port": 8501,
                "default_host": "localhost",
                "theme": "light"
            },
            "logging": {
                "level": "INFO",
                "log_file": "logs/valorant_coach.log"
            }
        }
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                
                # Merge with default config
                self._merge_config(self.config, file_config)
                logger.info(f"Configuration loaded from {self.config_file}")
            else:
                logger.info("No configuration file found, using defaults")
                self._save_config()
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def _merge_config(self, base: Dict, update: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _save_config(self):
        """Save current configuration to file"""
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., "capture.fps")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., "capture.fps")
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def save(self):
        """Save current configuration to file"""
        self._save_config()
    
    def reload(self):
        """Reload configuration from file"""
        self._load_config()
    
    def get_capture_config(self) -> Dict[str, Any]:
        """Get capture configuration"""
        return self.config.get("capture", {})
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis configuration"""
        return self.config.get("analysis", {})
    
    def get_coaching_config(self) -> Dict[str, Any]:
        """Get coaching configuration"""
        return self.config.get("coaching", {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration"""
        return self.config.get("ui", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.config.get("logging", {})

# Global configuration instance
config = Config()