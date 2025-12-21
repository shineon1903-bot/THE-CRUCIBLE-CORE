import random

# Global state to simulate impact of failures
fuel_modifier = 0

def get_entropic_fuel_level():
    """
    Calculates the current Entropic Fuel level.
    Simulates a draining fuel source with occasional spikes from recycling.
    """
    global fuel_modifier

    # Base logic: Starts high, drains over time, sometimes refills.
    # We add the modifier which might be negative due to failures.
    fuel = 42.1 + random.uniform(-0.5, 0.5) + fuel_modifier

    # Slowly recover modifier towards 0
    if fuel_modifier < 0:
        fuel_modifier += 0.1

    return max(0, min(100, fuel))

def recycle_sigil():
    """
    Attempts to recycle a sigil to boost fuel.
    """
    global fuel_modifier
    fuel_modifier += 5
    return "SIGIL RECYCLED. FUEL LEVEL INCREASED."

def consume_failure(failure_reason="Unknown"):
    """
    Consumes a system failure, converting it into a penalty or effect.
    """
    global fuel_modifier
    # For now, failure consumes fuel (penalty)
    print(f"FAILURE CONSUMED: {failure_reason}")
    fuel_modifier -= 2.0
    return "FAILURE CONSUMED. ENTROPIC PENALTY APPLIED."
