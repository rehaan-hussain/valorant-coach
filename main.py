#!/usr/bin/env python3
"""
Valorant AI Coach - Main Application
"""

import sys
import os
import logging
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Valorant AI Coach")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port for Streamlit app"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for Streamlit app"
    )
    
    args = parser.parse_args()
    
    # Setup basic logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Valorant AI Coach...")
    
    try:
        # Set Streamlit configuration
        os.environ["STREAMLIT_SERVER_PORT"] = str(args.port)
        os.environ["STREAMLIT_SERVER_ADDRESS"] = args.host
        
        # Import and run the app
        from src.ui.streamlit_app import create_app
        create_app()
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()