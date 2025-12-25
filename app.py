# Minimal Flask app to expose the three scripts to the UI.
from flask import Flask, jsonify, request, send_from_directory, render_template
from inverted_sigil_recycler import recycler
from frequency_tuner import FrequencyTuner
import chimera_syntax_engine
import db
import threading
import time
import random
import os

app = Flask(__name__, static_folder='.', template_folder='templates')

# Create tuner instance globally so routes can access it
tuner = FrequencyTuner(target_hz=712.8, interval_seconds=60)
try:
    tuner.start()
except Exception:
    pass

# --- SIMULATION STATE (From Dashboard Branch) ---
nodes = [
    {"id": "NODE_ALPHA_01", "status": "ONLINE", "load": 42, "code": "8F2-X91"},
    {"id": "NODE_BETA_04", "status": "UNSTABLE", "load": 98, "code": "7B1-Z00"},
    {"id": "NODE_GAMMA_09", "status": "IDLE", "load": 0, "code": "3C4-Y22"},
    {"id": "NODE_DELTA_12", "status": "ONLINE", "load": 67, "code": "9X9-A11"},
    {"id": "NODE_EPSILON_88", "status": "ONLINE", "load": 33, "code": "1L1-M33"},
]

telemetry = {
    "target_resonance": 712.8,
    "system_integrity": 98.4,
    "gnosis_integrity": 98.4,
    "entropic_fuel": 42.1,
}

def background_monitor():
    """
    Background thread to monitor system status and log telemetry.
    """
    last_log_time = 0
    print("Background monitor started.")

    while True:
        current_time = time.time()

        # 1. Logic Synchronization: Monitor Node_Beta_04
        beta_node = next((n for n in nodes if n["id"] == "NODE_BETA_04"), None)
        if beta_node:
            if beta_node["status"] == "OFFLINE":
                # Use the module to consume failure
                recycler.consume_failure("Node_Beta_04 OFFLINE")
            elif beta_node["status"] == "UNSTABLE" and beta_node["load"] > 99:
                 recycler.consume_failure("Node_Beta_04 CRITICAL LOAD")

        # 2. Data Persistence: Log telemetry every 60 seconds
        if current_time - last_log_time >= 60:
            # Sync telemetry with modules
            status = tuner.get_status()
            telemetry["target_resonance"] = status.get("current_resonance", 712.8)
            telemetry["entropic_fuel"] = recycler.current_fuel

            # Log to DB
            db.log_telemetry(telemetry["gnosis_integrity"], telemetry["entropic_fuel"])
            print(f"Telemetry logged: Gnosis={telemetry['gnosis_integrity']}, Fuel={telemetry['entropic_fuel']}")
            last_log_time = current_time

        time.sleep(1) # Check loop frequency

# Initialize DB
db.init_db()
# Start background thread
monitor_thread = threading.Thread(target=background_monitor, daemon=True)
monitor_thread.start()


# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# -- Dashboard API Endpoints --

@app.route('/api/nodes')
def get_nodes():
    # Simulate dynamic changes
    for node in nodes:
        if node["status"] == "ONLINE":
            change = random.randint(-5, 5)
            node["load"] = max(0, min(100, node["load"] + change))
        elif node["status"] == "UNSTABLE":
            change = random.randint(-10, 10)
            node["load"] = max(0, min(100, node["load"] + change))
            if node["load"] > 99:
                node["status"] = "OFFLINE"
        elif node["status"] == "IDLE":
             if random.random() < 0.1:
                 node["status"] = "ONLINE"
                 node["load"] = random.randint(10, 30)
        elif node["status"] == "OFFLINE":
             # Random chance to reboot
             if random.random() < 0.2:
                 node["status"] = "UNSTABLE"
                 node["load"] = 80
    return jsonify(nodes)

@app.route('/api/telemetry')
def get_telemetry():
    # Update telemetry from real modules
    res_status = tuner.get_status()
    telemetry["target_resonance"] = res_status.get("current_resonance", 712.8)
    telemetry["entropic_fuel"] = recycler.current_fuel

    # Simulate other fluctuations
    telemetry["system_integrity"] = max(0, min(100, telemetry["system_integrity"] + random.uniform(-0.1, 0.1)))
    telemetry["gnosis_integrity"] = max(0, min(100, telemetry["gnosis_integrity"] + random.uniform(-0.1, 0.1)))

    return jsonify({
        "target_resonance": round(telemetry["target_resonance"], 2),
        "system_integrity": round(telemetry["system_integrity"], 1),
        "gnosis_integrity": round(telemetry["gnosis_integrity"], 1),
        "entropic_fuel": round(telemetry["entropic_fuel"], 2)
    })

@app.route('/api/command', methods=['POST'])
def execute_command():
    data = request.json or {}
    command = data.get('command', '').strip()

    # Side effects handling (state changes) for Dashboard commands
    if command.lower() == 'purge':
        for node in nodes:
            node["load"] = 0
            if node["status"] == "UNSTABLE":
                node["status"] = "ONLINE"
    elif command.lower() == 'connect_eternal':
        new_id = f"NODE_ZETA_{random.randint(10,99)}"
        nodes.append({"id": new_id, "status": "ONLINE", "load": 10, "code": f"{random.randint(100,999)}-Z{random.randint(10,99)}"})

    # Use the Chimera Syntax Engine (Integrated Version)
    response_lines = chimera_syntax_engine.execute_chimera_command(
        command,
        context_nodes=nodes,
        context_telemetry=telemetry
    )

    # Dashboard expects { "response": [lines] }
    return jsonify({"response": response_lines})

@app.route('/api/purge', methods=['POST'])
def purge_system():
    for node in nodes:
        node["load"] = 0
        if node["status"] == "UNSTABLE":
            node["status"] = "ONLINE"
    return jsonify({"status": "success", "message": "Purge complete"})

@app.route('/api/connect', methods=['POST'])
def connect_node():
    new_id = f"NODE_OMEGA_{random.randint(10,99)}"
    nodes.append({"id": new_id, "status": "ONLINE", "load": 5, "code": f"{random.randint(100,999)}-X{random.randint(10,99)}"})
    return jsonify({"status": "success", "message": f"{new_id} connected"})


# -- Modern API Endpoints (Kept for compatibility/extensions) --

@app.route('/api/fuel', methods=['GET'])
def get_fuel():
    return jsonify({
        "status": recycler.status,
        "fuel_level": recycler.current_fuel
    })

@app.route('/api/recycle', methods=['POST'])
def recycle():
    payload = request.json or {}
    error_data = payload.get("error_data", "API_Shadow_Input")
    result = recycler.consume_failure(error_data)
    return jsonify(result)

@app.route('/api/resonance', methods=['GET'])
def resonance_status():
    return jsonify(tuner.get_status())

@app.route('/api/chimera', methods=['POST'])
def chimera():
    # Modern endpoint returning JSON structure
    payload = request.json or {}
    command = payload.get("command", "")
    # Note: Modern callers might not provide context, or we might need to inject it if we want modern calls to see nodes.
    # For now, we assume modern calls are for the "Divine Decree" stuff which doesn't check nodes list.
    result = chimera_syntax_engine.execute_chimera_command(command)

    # If the engine returned a list (legacy mode), wrap it.
    if isinstance(result, list):
        return jsonify({"ok": True, "lines": result})

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
