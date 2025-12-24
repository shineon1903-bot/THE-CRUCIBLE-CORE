# Minimal Flask app to expose the three scripts to the UI.
from flask import Flask, jsonify, request, send_from_directory
from inverted_sigil_recycler import recycler
from frequency_tuner import FrequencyTuner
from chimera_syntax_engine import execute_chimera_command
from mytho_quantum_core import TheWatchman
import threading
import os
import time
import db

app = Flask(__name__, static_folder='.')

# Create tuner instance globally so routes can access it
tuner = FrequencyTuner(target_hz=712.8, interval_seconds=60)

def start_background_tasks():
    # Initialize Database
    db.init_db()

    # Restore Fuel from Persistence
    last_telemetry = db.get_latest_telemetry()
    if last_telemetry:
        recycler.restore_fuel(last_telemetry['entropic_fuel'])
        print(f"Restored fuel level to {last_telemetry['entropic_fuel']}% from database.")

    # Start the frequency tuner
    try:
        tuner.start()
    except Exception:
        pass

    # Start TheWatchman (Node_Beta_04)
    watchman = TheWatchman(name="Node_Beta_04")
    # We assume a dummy error source for simulation
    def simulated_error_source(uptime):
        import random
        if random.random() < 0.1:
            return int(uptime % 10)
        return 0

    watchman.start_periodic_monitor(check_interval=45.0, error_source_callable=simulated_error_source)

    # Background thread for Telemetry Logging (Persistence)
    def telemetry_logger_loop():
        while True:
            try:
                current_fuel = recycler.current_fuel
                # Use current resonance as gnosis integrity proxy
                status = tuner.get_status()
                current_resonance = status.get('current_resonance', 0.0)

                db.log_telemetry(current_fuel, current_resonance)
            except Exception as e:
                print(f"Telemetry logging failed: {e}")

            time.sleep(60)

    telemetry_thread = threading.Thread(target=telemetry_logger_loop, daemon=True)
    telemetry_thread.start()

# Start background tasks if running as main
if __name__ == '__main__':
    start_background_tasks()
    app.run(host='127.0.0.1', port=5000, debug=True)


@app.route('/')
def index():
    # Serve index.html from the repo root (static_folder='.')
    return send_from_directory('.', 'index.html')

# Entropic Recycler endpoints
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

# Frequency tuner endpoint
@app.route('/api/resonance', methods=['GET'])
def resonance_status():
    return jsonify(tuner.get_status())

# Chimera console endpoint
@app.route('/api/chimera', methods=['POST'])
def chimera():
    payload = request.json or {}
    command = payload.get("command", "")
    result = execute_chimera_command(command)
    return jsonify(result)

if __name__ == '__main__':
    # Run Flask dev server
    app.run(host='127.0.0.1', port=5000, debug=True)
