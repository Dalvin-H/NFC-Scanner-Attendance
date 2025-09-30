import serial
import sqlite3

# Adjust to your COM port (Windows: COM3, Linux/Mac: /dev/ttyUSB0)
SERIAL_PORT = "COM4"
BAUD_RATE = 115200

# Create / connect to SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    uid TEXT PRIMARY KEY,
    name TEXT
)
""")
conn.commit()

# Example data (only added if not already in DB)
users = [
    ("A1B2C3D4", "Alice"),
    ("11223344", "Bob"),
    ("DEADBEEF", "Charlie"),
    ("A574959B", "Dalvin"),
]
for uid, name in users:
    cursor.execute("INSERT OR IGNORE INTO users (uid, name) VALUES (?, ?)", (uid, name))
conn.commit()

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

print("Listening for NFC scans...")

while True:
    line = ser.readline().decode("utf-8").strip()
    if not line:
        continue

    print(f"UID read: {line}")

    cursor.execute("SELECT name FROM users WHERE uid = ?", (line,))
    result = cursor.fetchone()

    if result:
        print(f"Hello, {result[0]}!")
    else:
        print("Unknown card")
