import sqlite3
from datetime import datetime, timezone

def init_db():
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    # creating a to store user warnings
    c.execute("""CREATE TABLE IF NOT EXISTS warnings(
              user_id INTEGER,
              guild_id INTEGER,
              reason TEXT,
              timestamp TEXT
              )    
        """)
    
    conn.commit()
    conn.close() #closing the DB connection

def add_warning(user_id, guild_id, reason):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()

    # Use a timezone-aware UTC datetime (recommended by Python and Discord.py)
    timestamp = datetime.now(timezone.utc).isoformat()

    c.execute(
        "INSERT INTO warnings (user_id, guild_id, reason) VALUES (?, ?, ?)",
        (user_id, guild_id, reason)
    )

    conn.commit()
    conn.close()

def get_warning(user_id, guild_id):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("SELECT reason, timestamp FROM warnings WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
    warnings = c.fetchall()  #Fetches all rows matching the query
    conn.close()
    return warnings