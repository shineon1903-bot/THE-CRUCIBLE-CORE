import random

def get_entropic_fuel_level():
    """
    Calculates the current Entropic Fuel level.
    Simulates a draining fuel source with occasional spikes from recycling.
    """
    # Base logic: Starts high, drains over time, sometimes refills.
    # In a real scenario, this might read from a sensor or database.
    # For now, we'll keep it simple but separate.

    # We can use a static variable or file to persist state if needed,
    # but for this simple scope, we'll just return a random value
    # biased around the previous logic but encapsulated here.

    # Let's assume a slight fluctuation for now.
    fuel = 42.1 + random.uniform(-0.5, 0.5)
    return max(0, min(100, fuel))

def recycle_sigil():
    """
    Attempts to recycle a sigil to boost fuel.
    """
    return "SIGIL RECYCLED. FUEL LEVEL INCREASED."
