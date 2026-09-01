import sqlite3

DB_FILE = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            status TEXT,
            date TEXT,
            sender TEXT,
            subject TEXT,
            gmail_message_id TEXT,
            last_updated TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            location TEXT,
            employment_type TEXT,
            deadline TEXT,
            url TEXT,
            jobtech_id TEXT,
            date_found TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dismissed_emails (
            gmail_message_id TEXT, date_dismissed TEXT
        )
    """)
  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_emails (
            gmail_message_id TEXT PRIMARY KEY,
            date_seen TEXT
        )
    """) 
  
    conn.commit()
    conn.close()




if __name__ == "__main__":
    init_db()
    print("Database initialized.")


import sqlite3
from datetime import datetime

DB_FILE = "tracker.db"

def save_application(company, role, status, date, sender, subject, gmail_message_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM applications WHERE company = ? AND role = ?", (company, role))
    existing = cursor.fetchone()
    now = datetime.now().isoformat()
    if existing:
        cursor.execute("""UPDATE applications SET status = ?, date = ?, sender = ?, subject = ?, gmail_message_id = ?, last_updated = ? WHERE id = ?""",
            (status, date, sender, subject, gmail_message_id, now, existing[0]))
    else:
        cursor.execute("""INSERT INTO applications (company, role, status, date, sender, subject, gmail_message_id, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (company, role, status, date, sender, subject, gmail_message_id, now))
    cursor.execute(
        "DELETE FROM opportunities WHERE LOWER(company) = LOWER(?) AND LOWER(role) = LOWER(?)",
        (company, role)
    )
    conn.commit()
    conn.close()

def save_opportunity(company, role, location, employment_type, deadline, url, jobtech_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM opportunities WHERE jobtech_id = ?", (jobtech_id,))
    existing = cursor.fetchone()
    cursor.execute("SELECT id FROM applications WHERE LOWER(company) = LOWER(?) AND LOWER(role) = LOWER(?)", (company, role))
    already_applied = cursor.fetchone()
    if not existing and not already_applied:
        now = datetime.now().isoformat()
        cursor.execute("""INSERT INTO opportunities (company, role, location, employment_type, deadline, url, jobtech_id, date_found) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (company, role, location, employment_type, deadline, url, jobtech_id, now))
    conn.commit()
    conn.close()

def is_already_processed(gmail_message_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT gmail_message_id FROM seen_emails WHERE gmail_message_id = ?", (gmail_message_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_email_seen(gmail_message_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO seen_emails (gmail_message_id, date_seen) VALUES (?, ?)", (gmail_message_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()