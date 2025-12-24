import sqlite3
import time
from typing import Dict, Any, Optional

DB_FILE = 'crucible.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initialize the database and create the soul_signature_telemetry table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS soul_signature_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            entropic_fuel REAL NOT NULL,
            gnosis_integrity REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_telemetry(entropic_fuel: float, gnosis_integrity: float):
    """Log a new telemetry record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO soul_signature_telemetry (timestamp, entropic_fuel, gnosis_integrity)
        VALUES (?, ?, ?)
    ''', (time.time(), entropic_fuel, gnosis_integrity))
    conn.commit()
    conn.close()

def get_latest_telemetry() -> Optional[Dict[str, Any]]:
    """Retrieve the most recent telemetry record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT entropic_fuel, gnosis_integrity, timestamp
        FROM soul_signature_telemetry
        ORDER BY id DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "entropic_fuel": row[0],
            "gnosis_integrity": row[1],
            "timestamp": row[2]
        }
    return None
