# database.py — Helper SQLite
import sqlite3

def get_db():
    conn = sqlite3.connect("siswa.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS tbsiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            alamat TEXT
        )
    """)
    db.commit()