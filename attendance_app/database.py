import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    uid TEXT PRIMARY KEY,
    name TEXT
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    name TEXT,
    status TEXT
)
""")
conn.commit()

def add_student(uid, name):
    cursor.execute("INSERT OR IGNORE INTO students (uid, name) VALUES (?, ?)", (uid, name))
    conn.commit()

def get_student(uid):
    cursor.execute("SELECT name FROM students WHERE uid = ?", (uid,))
    return cursor.fetchone()
