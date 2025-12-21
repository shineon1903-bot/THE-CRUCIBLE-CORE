# Minimal Flask app to expose the three scripts to the UI.
from flask import Flask, jsonify, request, send_from_directory
from inverted_sigil_recycler import recycler
from frequency_tuner import FrequencyTuner
from chimera_syntax_engine import execute_chimera_command
import threading
import os

app = Flask(__name__, static_folder='.')

# Start the frequency tuner in a background thread
tuner = FrequencyTuner(target_hz=712.8, interval_seconds=60)
truner = tuner
try:
    tuner.start()
except Exception:
    # If starting in certain execution contexts fails, ignore to keep import safe
    pass

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
