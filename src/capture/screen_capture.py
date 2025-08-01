"""
Thread-safe screen-capture helper for Valorant-AI-Coach
Creates its own mss() handle *inside* the worker thread, so it
never shares GDI device-contexts across threads (fixes 'srcdc' error).
"""

import threading
import time
from typing import Callable, Optional

import mss
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ScreenCapture(threading.Thread):
    """
    Capture frames in a background thread and send them to `callback(frame)`.
    """

    def __init__(
        self,
        monitor: int = 1,
        fps: int = 30,
        callback: Optional[Callable[[np.ndarray], None]] = None,
    ):
        super().__init__(daemon=True)
        self.monitor_idx = monitor
        self.interval = 1.0 / fps
        self.callback = callback
        self._running = threading.Event()

    # ---------- public API -------------------------------------------------
    def start_capture(self):
        """Start (or resume) the capture loop."""
        self._running.set()
        if not self.is_alive():
            self.start()

    def stop_capture(self):
        """Signal the thread to exit the capture loop cleanly."""
        self._running.clear()

    # ---------- thread entry-point ----------------------------------------
    def run(self):
        try:
            with mss.mss() as sct:  # mss handle lives only in THIS thread
                region = sct.monitors[self.monitor_idx]
                while self._running.is_set():
                    frame = np.array(sct.grab(region))
                    if self.callback:
                        self.callback(frame)
                    time.sleep(self.interval)
        except Exception as exc:
            logger.exception("Error capturing frame: %s", exc)