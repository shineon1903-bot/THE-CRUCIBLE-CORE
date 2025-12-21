import random

def execute_chimera_command(command, context_nodes=None, context_telemetry=None):
    """
    Parses and executes commands from the Chimera Syntax Console.

    Args:
        command (str): The command string entered by the user.
        context_nodes (list): Optional context about current nodes.
        context_telemetry (dict): Optional context about telemetry.

    Returns:
        list: A list of strings representing the output lines.
    """
    cmd = command.strip().lower()

    if cmd == 'init_sequence' or cmd == 'init_sequence --force':
        return [
            "INITIALIZING RITUAL SEQUENCE...",
            "LOADING 8k ASSETS [################----] 82%",
            "WARNING: Node_Beta_04 instability detected. Resonance mismatch.",
            "PARSING CHIMERA SYNTAX...",
            "SUCCESS. Protocol V.9.0 active."
        ]

    elif cmd == 'help':
        return [
            "CHIMERA SYNTAX CONSOLE V.9.0",
            "----------------------------",
            "Available Commands:",
            "  init_sequence    - Initialize system protocol",
            "  status           - Display system integrity and active nodes",
            "  purge            - Purge unstable nodes and clear cache",
            "  connect_eternal  - Establish connection with a new node",
            "  scan_resonance   - Analyze current frequency harmonics",
            "  help             - Display this help message"
        ]

    elif cmd == 'status':
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

    elif cmd == 'purge':
        # Note: The actual state change should happen in the caller (app.py) or via a callback,
        # but here we return the text response. The prompt implies this function handles the logic.
        # However, since this is a pure function engine, we might need to return instructions
        # or assume app.py handles side effects.
        # For this task, we'll return the text, and app.py will handle the side effects as before,
        # OR we can make this return a dict with action + message.
        # Let's stick to text for the "display" requirement, but app.py needs to handle the logic.
        # To strictly follow "sends input directly... and displays return message",
        # I'll return the message. app.py will need to handle the side effects separately or check command.
        return ["PURGE SEQUENCE INITIATED...", "CACHE CLEARED", "ALL SYSTEMS NORMALIZED"]

    elif cmd == 'connect_eternal':
        return ["CONNECTING NEW ETERNAL...", "SEARCHING FOR SIGNAL...", "CONNECTION ESTABLISHED."]

    elif cmd == 'scan_resonance':
        return [
            "SCANNING FREQUENCIES...",
            f"DETECTED HARMONIC: {random.uniform(700, 800):.2f} Hz",
            "WAVEFORM: STABLE"
        ]

    else:
        return [
            f"SYNTAX ERROR: Command '{command}' not recognized.",
            "Type 'help' for a list of valid commands."
        ]
