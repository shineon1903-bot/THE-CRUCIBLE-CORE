import time
import random

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

    return round(base_resonance + fluctuation, 2)
