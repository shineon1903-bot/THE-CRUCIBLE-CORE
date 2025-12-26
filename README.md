# THE-CRUCIBLE-CORE
The Crucible Dashboard

## Overview
The Crucible is a dashboard application that monitors system telemetry, manages "Soul Signature" nodes, and executes "Chimera Syntax" commands. It features a Flask backend and a dynamic HTML frontend.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd THE-CRUCIBLE-CORE
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the application:**
    ```bash
    python3 app.py
    ```

2.  **Access the Dashboard:**
    Open your web browser and navigate to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## API Endpoints

*   `GET /api/telemetry`: Retrieve current system status (Resonance, Integrity, Fuel).
*   `GET /api/nodes`: Retrieve the status of all monitored nodes.
*   `POST /api/command`: Execute a Chimera Syntax command.
    *   Payload: `{"command": "status"}`
