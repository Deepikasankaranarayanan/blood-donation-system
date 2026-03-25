import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
reg_no TEXT,
department TEXT,
dept_no TEXT,
year TEXT,
blood_group TEXT,
phone TEXT,
donated TEXT,
last_donated DATE,
next_date DATE
)
""")

conn.commit()
conn.close()

print("Database Created")