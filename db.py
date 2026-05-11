import sqlite3
import json

DB = "claims.db"


# ================= INIT DATABASE =================

def init_db():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        validation TEXT,
        route TEXT,
        reason TEXT,
        risk INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ================= SAVE CLAIM =================

def save_claim(data, validation, route, reason, risk):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "INSERT INTO claims (data, validation, route, reason, risk) VALUES (?,?,?,?,?)",
        (
            json.dumps(data),
            json.dumps(validation),
            route,
            reason,
            risk
        )
    )

    conn.commit()
    conn.close()


# ================= GET CLAIMS =================

def get_claims():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM claims")

    rows = c.fetchall()

    conn.close()

    return rows