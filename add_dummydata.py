import sqlite3
from datetime import datetime

# Database file name
DB_FILE = "timeflow_data.db"

# Connect to the SQLite database (creates file if not exists)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Supervisors (
    supervisor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supervisor_name TEXT NOT NULL,
    supervisor_email TEXT UNIQUE NOT NULL,
    supervisor_pwd TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supervisor_id INTEGER NOT NULL,
    employee_name TEXT NOT NULL,
    employee_email TEXT UNIQUE NOT NULL,
    employee_phone TEXT NOT NULL,
    employee_pwd TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supervisor_id) REFERENCES Supervisors (supervisor_id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    event_type TEXT CHECK(event_type IN ('Check-in', 'Check-out')) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    location TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES Employees (employee_id) ON DELETE CASCADE
);
""")

# Dummy Data
supervisors = [
    ("Alice Johnson", "alice@company.com", "hashed_pwd_1", datetime(2025, 3, 1, 8, 0)),
    ("Bob Williams", "bob@company.com", "hashed_pwd_2", datetime(2025, 3, 2, 9, 15)),
    ("Charlie Thompson", "charlie@company.com", "hashed_pwd_3", datetime(2025, 3, 3, 10, 30)),
]

employees = [
    (1, "David Smith", "david@company.com", "1234567890", "hashed_pwd_4", datetime(2025, 3, 4, 8, 0)),
    (1, "Emily Davis", "emily@company.com", "9876543210", "hashed_pwd_5", datetime(2025, 3, 5, 9, 15)),
    (1, "Frank Wilson", "frank@company.com", "5556667777", "hashed_pwd_6", datetime(2025, 3, 6, 10, 30)),
    (2, "Grace Miller", "grace@company.com", "4445556666", "hashed_pwd_7", datetime(2025, 3, 7, 11, 45)),
    (2, "Henry Moore", "henry@company.com", "3334445555", "hashed_pwd_8", datetime(2025, 3, 8, 12, 0)),
    (2, "Isabella Lee", "isabella@company.com", "2223334444", "hashed_pwd_9", datetime(2025, 3, 9, 13, 15)),
    (3, "Jack Anderson", "jack@company.com", "1112223333", "hashed_pwd_10", datetime(2025, 3, 10, 14, 30)),
    (3, "Kelly Brown", "kelly@company.com", "9998887777", "hashed_pwd_11", datetime(2025, 3, 11, 15, 45)),
    (3, "Liam White", "liam@company.com", "8887776666", "hashed_pwd_12", datetime(2025, 3, 12, 16, 0)),
]

attendance = [
    (1, "Check-in", datetime(2025, 3, 8, 8, 1), "1600 Amphitheatre Pkwy, Mountain View, CA"),
    (1, "Check-out", datetime(2025, 3, 8, 17, 5), "1600 Amphitheatre Pkwy, Mountain View, CA"),
    (2, "Check-in", datetime(2025, 3, 8, 9, 15), "Times Square, New York, NY"),
    (2, "Check-out", datetime(2025, 3, 8, 18, 0), "Times Square, New York, NY"),
    (3, "Check-in", datetime(2025, 3, 8, 10, 0), "London Bridge, London, UK"),
    (3, "Check-out", datetime(2025, 3, 8, 19, 0), "London Bridge, London, UK"),
    (4, "Check-in", datetime(2025, 3, 8, 8, 30), "Eiffel Tower, Paris, France"),
    (4, "Check-out", datetime(2025, 3, 8, 17, 45), "Eiffel Tower, Paris, France"),
    (5, "Check-in", datetime(2025, 3, 8, 7, 45), "Sydney Opera House, Sydney, Australia"),
    (5, "Check-out", datetime(2025, 3, 8, 16, 30), "Sydney Opera House, Sydney, Australia"),
]

# Insert Data
cursor.executemany("INSERT INTO Supervisors (supervisor_name, supervisor_email, supervisor_pwd, created_at) VALUES (?, ?, ?, ?)", supervisors)
cursor.executemany("INSERT INTO Employees (supervisor_id, employee_name, employee_email, employee_phone, employee_pwd, created_at) VALUES (?, ?, ?, ?, ?, ?)", employees)
cursor.executemany("INSERT INTO Attendance (employee_id, event_type, event_time, location) VALUES (?, ?, ?, ?)", attendance)

# Commit and close
conn.commit()
conn.close()

print("✅ Database initialized with dummy data!")
