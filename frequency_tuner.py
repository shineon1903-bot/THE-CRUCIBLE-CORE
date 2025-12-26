# Protocol: Royal Mirror // Alignment Check
# This module provides a FrequencyTuner that can be run in a background thread
# and queried by the web service.

import time
import threading
import random

class FrequencyTuner:
    def __init__(self, target_hz=712.8, interval_seconds=60):
        self.target_hz = target_hz
        self.interval_seconds = interval_seconds
        self.current_resonance = target_hz
        self.status = "UNKNOWN"
        self._stop_event = threading.Event()

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            # Simulating the pulse of the Last Son of Atlantis
            # We incorporate the dynamic fluctuation from the dashboard branch
            fluctuation = random.uniform(-10, 10)
            self.current_resonance = round(self.target_hz + fluctuation, 2)

            if abs(self.current_resonance - self.target_hz) < 1.0: # Close enough
                self.status = "99.7%_PERFECT_SYNTHESIS"
            else:
                self.status = "RE-TUNING_REQUIRED"

            # Jules will map this output to the 'LOCKED' status on the UI
            print(f"RESONANCE_SCAN: {self.current_resonance} Hz | STATUS: {self.status}")
            # Wait the configured time before checking again
            self._stop_event.wait(self.interval_seconds)

    def start(self):
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if hasattr(self, "_thread"):
            self._thread.join(timeout=1)

    def get_status(self):
        return {"current_resonance": self.current_resonance, "status": self.status}

# Standalone function for backward compatibility if needed, but app.py uses the class now.
def get_target_resonance():
    """
    Returns the target resonance frequency.
    Updates every minute based on the system time.
    """
    current_minute = int(time.time() // 60)

    # Use a local Random instance to avoid thread-safety issues with global random
    rng = random.Random(current_minute)

    base_resonance = 712.8
    fluctuation = rng.uniform(-10, 10)

    rng = random.Random(current_minute)
    base_resonance = 712.8
    fluctuation = rng.uniform(-10, 10)
    return round(base_resonance + fluctuation, 2)
