from flask import Flask, render_template, jsonify, request
import random
import datetime
import inverted_sigil_recycler
import frequency_tuner
import chimera_syntax_engine

app = Flask(__name__)

# Simulated Database
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

@app.route('/')
def index():
    return render_template('index.html')

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

    return jsonify(nodes)

@app.route('/api/telemetry')
def get_telemetry():
    # Use external modules for specific values
    telemetry["target_resonance"] = frequency_tuner.get_target_resonance()
    telemetry["entropic_fuel"] = inverted_sigil_recycler.get_entropic_fuel_level()

    # Simulate other fluctuations internally for now
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
    data = request.json
    command = data.get('command', '').strip()

    # Side effects handling (state changes)
    # Ideally, the engine might return a structured object indicating actions,
    # but for this requirement, we'll keep the side effects here or triggered by the command name.

    if command == 'purge':
        # Apply purge logic
        for node in nodes:
            node["load"] = 0
            if node["status"] == "UNSTABLE":
                node["status"] = "ONLINE"
    elif command == 'connect_eternal':
        new_id = f"NODE_ZETA_{random.randint(10,99)}"
        nodes.append({"id": new_id, "status": "ONLINE", "load": 10, "code": f"{random.randint(100,999)}-Z{random.randint(10,99)}"})

    # Use the Chimera Syntax Engine for the response text
    response_lines = chimera_syntax_engine.execute_chimera_command(
        command,
        context_nodes=nodes,
        context_telemetry=telemetry
    )

    return jsonify({"response": response_lines})

@app.route('/api/purge', methods=['POST'])
def purge_system():
     # Same logic as command 'purge'
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
