import sqlite3
import datetime

DB_NAME = "crucible.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS soul_signature_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                gnosis_integrity REAL,
                entropic_fuel REAL
            )
        ''')
    conn.close()

def log_telemetry(gnosis, fuel):
    conn = get_db_connection()
    with conn:
        conn.execute('''
            INSERT INTO soul_signature_telemetry (gnosis_integrity, entropic_fuel)
            VALUES (?, ?)
        ''', (gnosis, fuel))
    conn.close()

def get_telemetry_history(limit=10):
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM soul_signature_telemetry ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
