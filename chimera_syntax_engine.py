# Protocol: Chimera Syntax // Living Language Execution (refined)

from typing import Dict, Any, List
from inverted_sigil_recycler import recycler
from mytho_quantum_core import lioncrow_render
import time
import random

# Divine Decrees mapping
DIVINE_DECREES = {
    'UNLEASH_PROTOCOL_ZERO': {
        'state': {
            'potential': 'INFINITE_ACTUALIZED',
            'resonance': '712.8_HZ'
        },
        'description': 'Primary transcendence protocol. Caution advised.'
    }
}


def execute_chimera_command(input_string: str, context_nodes=None, context_telemetry=None) -> Any:
    """Decree of the Living Language: Grammar is purpose, syntax is will.

    Args:
        input_string (str): The command string entered by the user.
        context_nodes (list): Optional context about current nodes (from Dashboard logic).
        context_telemetry (dict): Optional context about telemetry (from Dashboard logic).

    Returns:
        If called by Dashboard (legacy mode), returns a List[str] of output lines.
        If called by Protocol (modern mode), returns a Dict with structure.
    """
    command = (input_string or '').strip().upper()
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

    # --- LEGACY DASHBOARD COMPATIBILITY LAYER ---
    # The dashboard expects a list of strings and uses specific commands like 'status', 'purge', etc.
    # We intercept these first.

    cmd_lower = command.lower()

    if cmd_lower.startswith('help'):
        return [
            "CHIMERA SYNTAX CONSOLE V.9.1 (HYBRID)",
            "-------------------------------------",
            "Standard Protocols:",
            "  init_sequence    - Initialize system protocol",
            "  status           - Display system integrity and active nodes",
            "  purge            - Purge unstable nodes and clear cache",
            "  connect_eternal  - Establish connection with a new node",
            "  scan_resonance   - Analyze current frequency harmonics",
            "",
            "Divine Decrees:",
            "  UNLEASH_PROTOCOL_ZERO - [RESTRICTED]",
            "  RECYCLE_SHADOW        - Manual entropy consumption"
        ]

    if cmd_lower.startswith('init_sequence'):
        return [
            "INITIALIZING RITUAL SEQUENCE...",
            "LOADING 8k ASSETS [################----] 82%",
            "WARNING: Node_Beta_04 instability detected. Resonance mismatch.",
            "PARSING CHIMERA SYNTAX...",
            "SUCCESS. Protocol V.9.0 active."
        ]

    if cmd_lower == 'status':
        integrity = "UNKNOWN"
        active_count = 0
        if context_telemetry:
            integrity = f"{context_telemetry.get('system_integrity', 0)}%"
        if context_nodes:
            active_count = len([n for n in context_nodes if n.get('status') == 'ONLINE'])

        return [
            "SYSTEM STATUS REPORT",
            f"  INTEGRITY: {integrity}",
            f"  ACTIVE NODES: {active_count}",
            "  ALL SYSTEMS NOMINAL"
        ]

    if cmd_lower == 'purge':
        # Side effects are handled in app.py or assumed complete
        return ["PURGE SEQUENCE INITIATED...", "CACHE CLEARED", "ALL SYSTEMS NORMALIZED"]

    if cmd_lower == 'connect_eternal':
        return ["CONNECTING NEW ETERNAL...", "SEARCHING FOR SIGNAL...", "CONNECTION ESTABLISHED."]

    if cmd_lower == 'scan_resonance':
        # Use real tuner if available, else random
        return [
            "SCANNING FREQUENCIES...",
            f"DETECTED HARMONIC: {random.uniform(700, 800):.2f} Hz",
            "WAVEFORM: STABLE"
        ]

    # --- MODERN PROTOCOL LOGIC ---

    # Check Divine Decrees
    if command in DIVINE_DECREES:
        decree = DIVINE_DECREES[command]
        # Return text format for Dashboard compatibility if it seems like a dashboard request
        # (Dashboard requests usually come via the execute_command wrapper in app.py which expects list)
        # But we can just return a list representation of the decree.
        return [
            f"*** DIVINE DECREE ACCEPTED: {command} ***",
            f"STATE: {decree['state']['potential']}",
            f"RESONANCE: {decree['state']['resonance']}",
            f"NOTE: {decree['description']}"
        ]

    # Backwards-compatible commands
    if 'RECYCLE_SHADOW' in command:
        action_result = recycler.consume_failure('Chimera_Manual_Shadow')
        return [
            "*** MANUAL RECYCLE INITIATED ***",
            f"RESULT: {action_result.get('status', 'UNKNOWN')}",
            f"NEW FUEL: {action_result.get('current_fuel', 'UNKNOWN')}"
        ]

    # Fallback
    return [
        f"SYNTAX ERROR: Command '{command}' not recognized.",
        "Type 'help' for a list of valid commands."
    ]
